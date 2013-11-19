from django.http import HttpResponse
from django.shortcuts import render

from django.utils.datastructures import SortedDict

from registration.models import RegistrationSession, Registration, MembershipCard, List, Person, QueryList, Person
from registration.models import autoList

from registration.lib import parseQueryList, ListParseException
from django.db.models import Q

from datetime import datetime

import json

from django.contrib.auth.decorators import login_required, permission_required

from registration import lib

from cStringIO import StringIO

import xlsxwriter

headers = {
	'first_name': 'First Name',
	'last_name': 'Last Name',
	'name': 'Name',
	'gender': 'Gender',
	'phone_number': 'Phone Number',
	'peoplesoft_number': 'Peoplesoft Number',
	'netid': 'NetID',
	'hometown': 'Hometown',
	'major': 'Major',
	'person_id': 'Person ID',
	'emails': 'All e-mail address(es)',
	'preferred_emails': 'E-mail address(es) the user preferrers',
	'uconn_email': 'E-mail address',
	'membership_card': 'Membership Card',
	'registration_session': 'Semester',
	'usg_person_type': 'Registration Classification',
	'semester_standing': 'Semester Standing',
	'person_type': 'Registration Classification',
	'team': 'Team/Club',
	'paid_amount': 'Amount Paid',
	'paid_date': 'Paid Date',
	'registration_id': 'Registration ID',
}

personAttrs = {
	'first_name': 'first_name',
	'last_name': 'last_name',
	'gender': 'gender',
	'phone_number': 'phone_number',
	'peoplesoft_number': 'peoplesoft_number',
	'netid': 'netid',
	'hometown': 'hometown',
	'major': 'major',
	'person_id': 'id',
	'name': 'name',
}

personTypeAttrs = {
	'usg_person_type': 'usg_person_type',
	'semester_standing': 'csc_semester_standing',
	'person_type': 'description'
}

registrationAttrs = {
	'registration_id': 'id',
	'paid_amount': 'paid_amount'
}

registrationRequiredExtra = ('membership_card', 'registration_session', 'team', 'paid_amount', 'paid_date')

registrationRequiredFields = set(registrationAttrs.keys()) | set(registrationRequiredExtra) | set(personTypeAttrs.keys())

def autocompleteQuery(searchArgs, inSession=None):
	q = Q()
	
	if inSession:
		q = Q(registration__registration__session__in=inSession)
	
	for token in searchArgs:
		tokenSearch = Q(first_name__icontains=token) | Q(last_name__icontains=token) | Q(emails__email__icontains=token)
		if q == None:
			q = tokenSearch
		else:
			q = q & tokenSearch
			
	return Person.objects.filter(q).distinct()
			

@login_required
def index(request):
	templateVars = {}
	templateVars["default_club_entry_list"] = "Entry %s" % datetime.today().strftime("%Y-%m-%d")
	templateVars["query_lists"] = QueryList.objects.all().order_by('slug')
	
	return render(request, "dashboard_index.html", templateVars)

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
	
@permission_required('registration.can_autocomplete')
def autocomplete(request):
	searchQ = request.GET.get("term", None)
	sessionsQ = request.GET.getlist("session", None)
	
	if not searchQ:
		return []
	
	#Get the base person query	
	query = autocompleteQuery(searchQ.split(" "))
	
	#Add on the registration session filter
	if sessionsQ:
		sessions = RegistrationSession.objects.filter(card_code__in=sessionsQ)
		
		query = query.filter(registration__registration_session__in=sessions)
	
	#Grab emails - not done above to limit the table scan of emails
	query = query.prefetch_related('emails')
	
	out = []
	
	for person in query:
		out.append({'id': person.id, 'first_name': person.first_name, 'last_name': person.last_name, 'emails': [e.email for e in person.emails.all()]})
		
	response = HttpResponse(content_type="application/json")
	json.dump(out, response)
	return response

@permission_required('registration.can_run_reports')
def reporting(request):
	if "process" in request.GET:
		return report(request)
	
	managedLists = {}
	
	for l in List.objects.exclude(list_type__in=['admin_list', 'entry_list']):
		listType = l.get_list_type_display()
		if listType not in managedLists:
			managedLists[listType] = {}
			
		semester, listName = l.slug.split('-', 1)
		if semester not in managedLists[listType]:
			managedLists[listType][semester] = []
		managedLists[listType][semester].append(l)
	
	sortedManagedLists = SortedDict()
			
	for listType in managedLists:
		sortedManagedLists[listType] = SortedDict()
		
		semestersDict = managedLists[listType]
		
		for semesterCode in reversed(sorted(semestersDict, key=lib.registrationCardCodeKey)):
			sortedManagedLists[listType][semesterCode] = sorted(semestersDict[semesterCode], key=lambda x: x.name)
			
	unmanagedLists = List.objects.filter(list_type__in=['admin_list']).order_by('name')
		
	return render(request, "dashboard_reporting.html", 
	{'registration_sessions': reversed(sorted(RegistrationSession.objects.all(), key=lambda rs: lib.registrationCardCodeKey(rs.card_code))), 
	'managed_lists': sortedManagedLists,
	'unmanaged_lists': unmanagedLists,
	'query_lists': QueryList.objects.all()})
	
@permission_required('registration.can_run_reports')
def report(request):
	try:
		people = parseQueryList(request.GET["query"], "\n")
	except ListParseException, e:
		return HttpResponse("Error processing list query: %s" % e.s)
		
	fields = request.GET["fields"].splitlines()
	registrationSessions = [RegistrationSession.objects.get(card_code=x) for x in request.GET["registration_sessions"].splitlines() if x]
	
	registrationRequired = False
	
	for f in fields:
		if f in registrationRequiredFields:
			registrationRequired = True
	
	rows = []
	
	def getRegistration(p):
		for rs in registrationSessions:
			try:
				return Registration.objects.get(person=p, registration_session=rs)
			except Registration.DoesNotExist:
				continue
	try:
		header = [headers[f] for f in fields]
	except KeyError:
		return HttpResponse("There was an invalid field. Please check your query")
	data = []
	
	for p in sorted(people, key=lambda x: (x.last_name, x.first_name)):
		row = []
		
		if registrationRequired:
			registration = getRegistration(p)
		else:
			registration = None
			
		for f in fields:
			if f in personTypeAttrs:
				if registration:
					row.append(getattr(registration.person_type, personTypeAttrs[f]))
				else:
					row.append("Unknown")
				
				continue
					
			if f in personAttrs:
				row.append(getattr(p, personAttrs[f]))
			
				continue
				
			if f in registrationAttrs:
				if registration:
					row.append(getattr(registration, registrationAttrs[f]))
				else:
					row.append("Unknown")
			
				continue
				
			if f == 'membership_card':
				if registration:
					try:
						mc = MembershipCard.objects.get(registration=registration)
						row.append(mc.membership_card)
					except MembershipCard.DoesNotExist:
						row.append("None")
				else:
					row.append("None")
					
				continue
				
			if f == 'registration_session':
				if registration:
					row.append(registration.registration_session.card_code)
				else:
					row.append("Unknown")
				
				continue
					
			if f == 'gender':
				if p.gender == 'M':
					row.append('Male')
				elif p.gender == 'F':
					row.append('Female')
				else:
					row.append("Unknown")
				
				continue
			
			if f == 'team':
				if registration and registration.team:
					row.append('Team')
				elif registration and not registration.team:
					row.append('Club')
				else:
					row.append("Unknown")
				
				continue
					
			if f == 'paid_date':
				if registration and registration.paid_date:
					row.append(registration.paid_date.strftime("%Y-%m-%d"))
				else:
					row.append("N/A")
				
				continue	
		
			if f == 'emails':
				row.append(", ".join([e.email for e in p.emails.all()]))
				
				continue
				
			if f == 'preferred_emails':
				row.append(", ".join([e.email for e in p.emails.filter(send=True)]))
				
				continue
				
			if f == 'uconn_email':
				row.append(", ".join([e.email for e in p.emails.filter(email__contains="@uconn.edu")]))
				
				continue
				
			
				
		data.append(row)
	
	if request.GET['format'] == 'HTML':			
		return render(request, "dashboard_report.html", {'data': data, 'header': header, 'count': len(data)})
	elif request.GET['format'] == 'Excel':
		out = StringIO()
		
		workbook = xlsxwriter.Workbook(out)
		worksheet = workbook.add_worksheet()
		
		bold = workbook.add_format({'bold': 1})
		
		for i, h in enumerate(header):
			worksheet.write(0, i, h, bold)
		
		for i, row in enumerate(data):
			for j, item in enumerate(row):
				worksheet.write(i+1, j, item)
				
		workbook.close()
		
		response = HttpResponse(content_type='application/vnd.ms-excel')
		response['Content-Disposition'] = 'filename="roster.xlsx"'
		
		response.write(out.getvalue())
		
		return response