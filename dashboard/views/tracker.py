from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from registration import lib

import lists.models
import lists.lib
import registration.lib

import json
import logging

log = logging.getLogger(__name__)

@permission_required('registration.entry_tracker')
def record_entry(request):
	queryListSlug = request.POST["verify_list"]
	recordListName = request.POST["record_list"]
	search_code = request.POST["entry_code"]
	
	queryList = lists.models.QueryList.objects.get(slug=queryListSlug)
	person = registration.lib.autoPerson(lib.codeSearch(search_code))
	
	queryListPeople = queryList.people
	
	if not person:
		response = HttpResponse(content_type="application/json")
		json.dump({'allowed': False, 'person_found': False}, response)
		return response
		
	
	if person in queryListPeople:
		response = HttpResponse(content_type="application/json")
		json.dump({'allowed': True, 'person_found': True, 'first_name': person.first_name, 'last_name': person.last_name}, response)
		entryList = lists.lib.autoList(recordListName, 'entry_list')
		entryList.people.add(person)
		entryList.save()
		log.info("Recording entry for %s into %s" % (person, entryList))
		return response
	else:
		response = HttpResponse(content_type="application/json")
		json.dump({'allowed': False, 'person_found': True, 'first_name': person.first_name, 'last_name': person.last_name}, response)
		return response