#!/usr/bin/python

import psycopg2
import psycopg2.extras

from ballroomcms import settings_production as settings
from django.core.management import setup_environ
setup_environ(settings)

from django.core.exceptions import ObjectDoesNotExist

from django.db import transaction
from registration import models

from django.template.defaultfilters import slugify

conn = psycopg2.connect("dbname='ballroom' user='www-ballroom' host='combo1.peacockhosting.net' password='ubdance123'")

sessionMap = {}
personMap = {}
personTypeMap = {}

def main():
	with transaction.commit_on_success():
		registrationSessions()
		people()
		emails()
		personTypes()
		registrations()
		
def registrations():
	for o in [models.Registration.objects.all()]:
		o.delete()
	
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("SELECT * FROM registration.registrations")
	
	
	
	for row in cur:
		print row
		r = models.Registration()
		r.person = personMap[row["person_id"]]
		r.registration_session = sessionMap[row["session_id"]]
		r.person_type = personTypeMap[row["person_type_id"]]
		r.team = row["team"]
		r.sent_registration_email = row["sent_registration_email"]
		
		if row["paid_amount"] == None:
			r.paid_amount = 0
			r.fee_waived = False
		elif row["paid_amount"] == 0:
			r.paid_amount = 0
			r.fee_waived = True
		else:
			r.paid_amount = row["paid_amount"]
			if row["paid_date"]:
				r.paid_date = row["paid_date"]
		
		r.team = row["team"]
				
		if row["membership_card"]:
			r.save()
			mc = models.MembershipCard()
			mc.membership_card = row["membership_card"]
			mc.registration = r
			mc.save()
		else:
			r.save()
		
			
		
	
def personTypes():
	for o in [models.PersonType.objects.all()]:
		o.delete()
		
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("SELECT * FROM registration.person_types")
	
	for row in cur:
		print row
		pt = models.PersonType()
		personTypeMap[row["id"]] = pt
		
		for a in ('description', 'student_rate', 'uconn_student', 'usg_person_type', 'csc_semester_standing'):
			if row[a]:
				setattr(pt, a, row[a])
		
		pt.enabled = row["show"]
			
		pt.save()
	
		
def people():
	for o in [models.Person.objects.all()]:
		o.delete()

	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

	cur.execute("SELECT id, first_name, last_name, gender, phone_number, peoplesoft_number, hometown, netid, major FROM registration.people")
	
	for row in cur:
		print row
		p = models.Person()
		
		for a in ['first_name', 'last_name', 'gender', 'phone_number', 'peoplesoft_number', 'hometown', 'netid', 'major']:
			if row[a]:
				setattr(p, a, row[a])
		
		p.save()
		personMap[row["id"]] = p
		
def emails():
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("SELECT * FROM registration.email_addresses")
	
	for row in cur:
		print row["email_address"]
		e = models.PersonEmail()
		
		e.person = personMap[row["person_id"]]
		e.send = row["recieve_mail"]
		e.email = row["email_address"]
		e.save()
			
def registrationSessions():
	for o in [models.RegistrationSession.objects.all()]:
		o.delete()
	
	cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	cur.execute("""SELECT id, semester, year, base_price, team_surcharge, nonstudent_surcharge, early_discount, early_deadline, returning_discount, first_club_day, last_free_day from registration.registration_sessions""")

	for row in cur:
		print row
		rs = models.RegistrationSession()
		rs.year = row["year"]
		if row["semester"] == 'F':
			rs.semester = 'Fall'
		else:
			rs.semester = 'Spring'
	
		for a in ('base_price', 'team_surcharge', 'nonstudent_surcharge', 
			'early_discount', 'returning_discount', 'early_deadline', 
			'first_club_day', 'last_free_day'):
		
			setattr(rs, a, row[a])
		
		card_code = "%02d%s" % (row["year"]	- 2000, row["semester"])
		print card_code
		rs.card_code = card_code


	
		#Take care of list creation
		auto_names = (
			('club_paid_list', 'club', '-paid'),
			('club_unpaid_list', 'club', '-unpaid'),
			('team_paid_list', 'team', '-paid'),
			('team_unpaid_list', 'team', '-unpaid'),
		)
	
		for attr, autoPrefix, autoSuffix in auto_names:
			try:
				related_list = getattr(rs, attr)
			except ObjectDoesNotExist, e:
				related_list = None
		
			if not related_list:
				auto_list_name = "%s%s%s" % (autoPrefix, rs.card_code.lower(), autoSuffix)
				slug = slugify(auto_list_name)
				try:
					l = models.List.objects.get(slug=slug)
				except ObjectDoesNotExist, e:
					l = models.List(name=auto_list_name, slug=slug)
					l.save()

				setattr(rs, attr, l)
	
		rs.save()
		sessionMap[row["id"]] = rs
if __name__ == "__main__":
	main()