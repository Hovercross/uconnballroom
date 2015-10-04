from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from lists.models import QueryList
from lists.lib import autoList

from registration.lib import autoPerson, codeSearch

import logging

log = logging.getLogger(__name__)

@csrf_exempt
def record_entry(request):
    authKey = request.POST.get("auth_key") #Such a hack, but I'm feeling lazy
    
    if authKey != "adrifgyseirufgjseor8gy89werhguysodfy78aeyrfg678yw489ghwerytfge":
        return JsonResponse({'authenticated': False, 'recorded': False})
    
    search_code = request.POST["entry_code"]

    recordListSlug= "Entry %s" % datetime.today().strftime("%Y-%m-%d")
    queryListSlug = "club-entry"
    
    queryList = QueryList.objects.get(slug=queryListSlug)
    person = autoPerson(codeSearch(search_code))
    
    queryListPeople = queryList.people
    
    if not person:
        return JsonResponse({'authenticated': True, 'recorded': False, 'found': False})
    
    if person in queryListPeople:
        entryList = autoList(recordListSlug, 'entry_list')
        
        if entryList.list_type != 'entry_list':
            log.warning("Entry record attempt into a non-entry list")
            return JsonResponse({'authenticated': True, 'recorded': False, 'found': True, 'first_name': person.first_name, 'last_name': person.last_name, 'error': 'Entry record attempt into a non-entry list'})
        
        entryList.people.add(person)
        entryList.save()
        log.info("Recording entry for %s into %s" % (person, entryList))
        return JsonResponse({'authenticated': True, 'recorded': True, 'found': True, 'first_name': person.first_name, 'last_name': person.last_name})

    else:
        return JsonResponse({'authenticated': True, 'recorded': False, 'first_name': person.first_name, 'last_name': person.last_name, 'error': '{first:} {last:} is not allowed into the ballroom'.format(first=person.first_name, last=person.last_name)})