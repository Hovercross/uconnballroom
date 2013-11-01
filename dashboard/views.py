from django.http import HttpResponse
from django.shortcuts import render

from registration.models import RegistrationSession, Registration, MembershipCard, List
from registration.lib import parseQueryList

from django.contrib.auth.decorators import login_required, permission_required

from registration.lib import registrationCardCodeKey

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
	'preferred_emails': 'E-mail address(es)',
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

@login_required
def index(request):
	return render(request, "dashboard_index.html")

@permission_required('registration.can_run_reports')
def reporting(request):
	if "process" in request.GET:
		return report(request)
		
	return render(request, "dashboard_reporting.html", 
	{'registration_sessions': reversed(sorted(RegistrationSession.objects.all(), key=lambda rs: registrationCardCodeKey(rs.card_code))), 
	'basic_lists': List.objects.all().order_by('slug')})
	
@permission_required('registration.can_run_reports')
def report(request):
	people = parseQueryList(request.GET["query"], "\n")
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
	
	header = [headers[f] for f in fields]
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
				
	return render(request, "dashboard_report.html", {'data': data, 'header': header})