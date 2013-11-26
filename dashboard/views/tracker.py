from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

from registration import lib

from lists.models import QueryList

import lists.models
import lists.lib
import registration.lib

import json
import logging

from datetime import datetime

log = logging.getLogger(__name__)

@permission_required('registration.entry_tracker')
def index(request):
	templateVars = {}
	templateVars["default_club_entry_list"] = "Entry %s" % datetime.today().strftime("%Y-%m-%d")
	templateVars["query_lists"] = QueryList.objects.all().order_by('slug')
	
	return render(request, "dashboard_tracker.html", templateVars)
	

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
		
		if entryList.list_type != 'entry_list':
			log.warning("Entry record attempt into a non-entry list")
			return HttpResponseBadRequest("You cannot record into a list type other than entry")
		
		entryList.people.add(person)
		entryList.save()
		log.info("Recording entry for %s into %s" % (person, entryList))
		return response
	else:
		response = HttpResponse(content_type="application/json")
		json.dump({'allowed': False, 'person_found': True, 'first_name': person.first_name, 'last_name': person.last_name}, response)
		return response