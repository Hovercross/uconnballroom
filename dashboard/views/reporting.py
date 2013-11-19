from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.datastructures import SortedDict

from registration.models import List, Person, RegistrationSession, QueryList
from registration.lib import parseQueryList, ListParseException
from registration import lib

import xlsxwriter
from cStringIO import StringIO

#All available report headers, used for report display
HEADERS = {
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

#Attributes that can be lifted straight off the person record
PERSONATTRS = {
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

#Attributes that can me lifted straight off the registration.person_type record
PERSONTYPEATTRS = {
	'usg_person_type': 'usg_person_type',
	'semester_standing': 'csc_semester_standing',
	'person_type': 'description'
}

#Attributes that can be lifted straight off the registration record
REGISTRATIONATTRS = {
	'registration_id': 'id',
	'paid_amount': 'paid_amount'
}

#Attributes that require the registration to be completed, aside from those listed in the direct accessors above
REGISTRATIONREQUIREDEXTRAATTRS = ('membership_card', 'registration_session', 'team', 'paid_amount', 'paid_date')

#Attributes that will require the registration to be computed
REGISTRATIONREQUIREDFIELDS = set(REGISTRATIONATTRS.keys()) | set(REGISTRATIONREQUIREDEXTRAATTRS) | set(PERSONTYPEATTRS.keys())


def reportData(people, fields, sessionPriority):
	registrationRequired = False
	
	for f in fields:
		if f in REGISTRATIONREQUIREDFIELDS:
			registrationRequired = True
	
			rows = []

			def getRegistration(p):
				for rs in registrationSessions:
					try:
						return Registration.objects.get(person=p, registration_session=rs)
					except Registration.DoesNotExist:
						continue

	for p in sorted(people, key=lambda x: (x.last_name.lower(), x.first_name.lower())):
		row = []

		if registrationRequired:
			registration = getRegistration(p)
		else:
			registration = None

		for f in fields:
			if f in PERSONTYPEATTRS:
				if registration:
					row.append(getattr(registration.person_type, PERSONTYPEATTRS[f]))
				else:
					row.append("Unknown")

				continue

			if f in PERSONATTRS:
				row.append(getattr(p, PERSONATTRS[f]))

				continue

			if f in REGISTRATIONATTRS:
				if registration:
					row.append(getattr(registration, REGISTRATIONATTRS[f]))
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



		yield row

def htmlReport(request, headers, data):
	data = list(data)
	return render(request, "dashboard_report.html", {'data': data, 'headers': headers, 'count': len(data)})
	
def excelReport(request, headers, data):
	out = StringIO()
	
	workbook = xlsxwriter.Workbook(out)
	worksheet = workbook.add_worksheet()
	
	bold = workbook.add_format({'bold': 1})
	
	for i, h in enumerate(headers):
		worksheet.write(0, i, h, bold)
	
	for i, row in enumerate(data):
		for j, item in enumerate(row):
			worksheet.write(i+1, j, item)
			
	workbook.close()
	
	response = HttpResponse(content_type='application/vnd.ms-excel')
	response['Content-Disposition'] = 'filename="roster.xlsx"'
	
	response.write(out.getvalue())
	
	return response

@permission_required('registration.can_run_reports')
def index(request):	
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
		return HttpResponse("Error parsing list: %s" % e.s)
	
	fields = [field for field in request.GET["fields"].splitlines() if field]
	
	registrationSessions = [RegistrationSession.objects.get(card_code=card_code) for card_code in request.GET["registration_sessions"].splitlines() if card_code]
	
	try:
		headers = [HEADERS[f] for f in fields]
	except KeyError:
		return HttpResponse("There was an invalid field. Please check your query")
	
	
	data = reportData(people, fields, registrationSessions)
	
	
	if request.GET['format'] == 'HTML':			
		return htmlReport(request, headers, data)
	elif request.GET['format'] == 'Excel':
		return excelReport(request, headers, data)