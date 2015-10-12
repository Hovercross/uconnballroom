import json
import hmac
import base64
import hashlib

from io import BytesIO
from datetime import datetime

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.contrib.auth.decorators import permission_required

from lists.models import RemoteScanEndpoint, RemoteScanUUID
from lists.lib import autoList
from registration.lib import autoPerson, codeSearch

import qrcode
import qrcode.image.svg


@csrf_exempt
def remoteScan(request, id):
    try:
        endpoint = RemoteScanEndpoint.objects.get(pk=id)
    except RemoteScanEndpoint.DoesNotExist:
        return JsonResponse({"alert": "Endpoint ID does not exist, please re-configure remote scanner", "remove": True})
    
    data = json.loads(request.body.decode("utf-8"))
    
    testSignature = data["uuid"] + data["timestamp"] + data["code"]
    
    remoteDigest = base64.decodebytes(data["signature"].encode())
    localDigest = hmac.new(endpoint.auth_key.encode(), testSignature.encode(), hashlib.sha256).digest()
    
    authPass = hmac.compare_digest(localDigest, remoteDigest)
    
    if not authPass:
        return JsonResponse({"alert_title": "Authentication Failure", "alert_message": "HMAC digest failure", "stop": True})
    
    person = autoPerson(codeSearch(data["code"]))
    
    if not person:
        return JsonResponse({"remove": 10, "alert_title": "Search Error", "alert_message": "Person not found with search code {code:}".format(code=data["code"])})
    
    if endpoint.allowed_list:
        checkList = endpoint.allowed_list
        checkPeople = endpoint.allowed_list.people
        
        if not person in checkPeople:
            return JsonResponse({"message": "Denied: {name:}".format(name=person.name), "remove": 10, "alert_title": "Entry Not Allowed", "alert_message": "{name} is not in {list}".format(name=person.name, list=endpoint.allowed_list.name)})
    
    with transaction.atomic():
        RemoteScanUUID(uuid=data["uuid"]).save()
        
        if endpoint.scan_list:
            scanList = endpoint.scan_list
        
        else:
            scanListSlug = "{prefix:} {date:}".format(prefix=endpoint.list_prefix, date=datetime.today().strftime("%Y-%m-%d"))
            scanList = autoList(scanListSlug, "entry_list")
        
        if person in scanList.people.all():
            duplicate = True
        else:
            duplicate = False
            scanList.people.add(person)
    
    params = {"remove": 3, "sound": "beep"}    
    if duplicate:
        params["message"] = "Duplicate: {name:}".format(name=person.name)
    else:
        params["message"] = "Allowed: {name:}".format(name=person.name)
    
    return JsonResponse(params)

@permission_required('lists.change_remotescanendpoint')
def remoteScanSetup(request, id):
    #TODO: Security
    
    endpoint = RemoteScanEndpoint.objects.get(pk=id)
    
    url = request.build_absolute_uri(reverse(remoteScan, kwargs={'id': endpoint.id}))
    
    data = {
        "remotescan": {
            "title": endpoint.title,
            "url": url,
            "signing_key": endpoint.auth_key,
            "code_types": ["QR"],
            "version": 1
        }
    }
    
    encodedData = json.dumps(data)
    
    img = qrcode.make(encodedData, image_factory=qrcode.image.svg.SvgPathImage, box_size=20)
    
    out = BytesIO()
    img.save(out)
    out.seek(0)
    
    return HttpResponse(out.read(), content_type="image/svg+xml")    