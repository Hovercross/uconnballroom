#!/usr/bin/env python

from ballroomcms import settings_production
from django.core.management import setup_environ
setup_environ(settings_production)

import sys

from registration.models import Registration
from cStringIO import StringIO
import csv
import unicodedata

out = open(sys.argv[1], "wb")

writer = csv.writer(out)

writer.writerow(['First Name', 'Last Name', 'Emails', 'Semester', 'Person Type', 'Team', 'Paid Amount', 'NetID', 'Peoplesoft', 'Phone'])

def stripUnicode(s):
	return unicodedata.normalize('NFKD', unicode(s)).encode('ascii','ignore')

for r in Registration.objects.all():
	emails = ", ".join([e.email for e in r.person.emails.all() if e.send])
	writer.writerow(map(stripUnicode, [r.person.first_name, r.person.last_name, emails, r.registration_session.card_code, r.person_type.description, r.team and 'Yes' or 'No', r.paid_amount or "", r.person.netid, r.person.peoplesoft_number, r.person.phone_number]))
	
out.close()
