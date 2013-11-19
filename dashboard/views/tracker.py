from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from registration.models import QueryList, autoList
from registration import lib

import json

@permission_required('registration.club_entry')
def record_entry(request):
	queryListSlug = request.POST["verify_list"]
	recordListName = request.POST["record_list"]
	search_code = request.POST["entry_code"]
	
	queryList = QueryList.objects.get(slug=queryListSlug)
	person = lib.autoPerson(lib.codeSearch(search_code))
	
	queryListPeople = queryList.people
	
	if not person:
		response = HttpResponse(content_type="application/json")
		json.dump({'allowed': False, 'person_found': False}, response)
		return response
		
	
	if person in queryListPeople:
		response = HttpResponse(content_type="application/json")
		json.dump({'allowed': True, 'person_found': True, 'first_name': person.first_name, 'last_name': person.last_name}, response)
		entryList = autoList(recordListName, 'entry_list')
		entryList.included_people.add(person)
		entryList.save()
		return response
	else:
		response = HttpResponse(content_type="application/json")
		json.dump({'allowed': False, 'person_found': True, 'first_name': person.first_name, 'last_name': person.last_name}, response)
		return response