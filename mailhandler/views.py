from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail, mail_managers

from mailhandler.models import MailingListMessage, MailingListMessageAttachment, MailSender
from lists.models import QueryList, List

import email.utils
import hashlib, hmac
import json
import requests


@csrf_exempt
def handleIncomingEmail(request):
	try:
		token = request.POST["token"]
		timestamp = int(request.POST["timestamp"])
		signature = request.POST["signature"]
	except KeyError:
		return HttpResponseForbidden("Signature incomplete")
		
	if not verify(token, timestamp, signature):
		return HttpResponseForbidden("Signature mismatch")
	
	sender = request.POST["sender"]
	recipient = request.POST["recipient"]
	from_name, from_address = email.utils.parseaddr(request.POST["from"])
	
	if request.POST.get('X-Mailgun-Spf', '').upper() == 'PASS':
		spfOK = True
	else:
		spfOK = False
	
	if request.POST.get('X-Mailgun-Dkim-Check-Result', '').upper == 'PASS':
		from_local, from_domain = from_address.split("@")
		from_domain = from_domain.lower()
		
		dkimData = dkimSplit(request.POST["Dkim-Signature"])
		
		dkim_domain = dkimData["d"].lower()
		signed_headers = map(str.lower, dkimDatap["h"].split(":"))
		
		if dkim_domain == from_domain and "from" in signed_headers:
			dkimOK = True
		else:
			dkimOK = False
	else:
		dkimOK = False
		
	#For autosending purposes, the sender must match the from address and be either SPF or DKIM OK
	if sender == from_address and (spfOK or dkimOK):
		senderVerified = True
	else:
		senderVerified = False
		
	subject = request.POST["subject"]
	body_text = request.POST["body-plain"]
	body_html = request.POST.get("body-html", None)
	message_id = request.POST.get("Message-Id", None)
	
	content_map = request.POST.get("content-id-map", None)
	
	try:
		toList = QueryList.objects.get(slug=recipient.split("@")[0])
	except QueryList.DoesNotExist:
		if not spfOK:
			#TODO: Mail admins?
			return HttpResponse("FAIL")
		else:
			send_mail("Error sending message to mailing list", "Error: The address %s is unknown to the UConn Ballroom e-mail system" % recipient, 'webmaster@uconnballroom.com', [sender])
			return HttpResponse("FAIL")
	
	try:
		mailSender = MailSender.objects.get(from_address=from_address)
		
		if mailSender.unrestricted_send:
			autoSend = True
		if toList in mailSender.send_to_lists.all():
			autoSend = True
			
		if mailSender.rewrite_from_name:
			from_name = mailSender.rewrite_from_name
		if mailSender.rewrite_from_address:
			from_address = mailSender.rewrite_from_address
			
	except MailSender.DoesNotExist:
		autoSend = False
	
	m = MailingListMessage()
	m.from_name = from_name
	m.from_address = from_address
	
	m.return_path = sender
	
	m.subject = subject
	
	m.body_text = body_text
	m.body_html = body_html
	
	m.message_id = message_id
	
	m.save()

	try:
		for p in toList.people:
			m.people.add(p)
	except List.DoesNotExist:
		mail_managers("Error sending e-mail to mailing list", "The query list %s is invalid" % toList.slug)
	
	attachments = {}
	
	for f in request.FILES:
		attachments[f] = {
			'attachment': request.FILES[f],
			'name': request.FILES[f].name,
			'cid': None
			}
			
	if content_map:
		for key, value in json.loads(content_map).items():
			key = key[1:-1]
			attachments[value]['cid'] = key
			
	
	for attachment in attachments.values():
		fileName = attachment['name']
		cid = attachment['cid']

		a = MailingListMessageAttachment()
		a.attachment = attachment['attachment']
		a.cid = cid
		a.message = m
		a.save()
	
	if autoSend:
		
		m.send()
	else:
		if senderVerified:
			m.sendHoldMessage()	
		mail_managers("New e-mail added to queue", "Message %d from %s has been added to the outgoing mail queue and requires attention." % (m.id, m.from_address))
		
	return HttpResponse("OK")


def dkimSplit(DKIMHeader):
	items = map(str.strip, DKIMHeader.split(";"))
	
	data = {}
	
	for i in items:
		key, value = i.split("=", 1)
		
		data[key] = value
		
	return data
	

def verify(token, timestamp, signature):
    return signature == hmac.new(
                             key=settings.MAILGUN_KEY,
                             msg='{}{}'.format(timestamp, token),
                             digestmod=hashlib.sha256).hexdigest()