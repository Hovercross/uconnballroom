from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.units import inch
from reportlab.graphics.barcode.code128 import Code128

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from django.core.mail import send_mail, EmailMessage

import models

from datetime import date

from qr import QRCodeFlowable

SEMESTERCODES = {'S': 1, 'F': 2}

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

def sendRegistrationEmail(registration):
	pass

def getRegistrationForm(registration):
	sample_styles = getSampleStyleSheet()
	normal = ParagraphStyle('normal', parent=sample_styles["Normal"])
	title = ParagraphStyle('title', sample_styles["Title"], fontSize=28, spaceAfter=.5*inch)
	heading = ParagraphStyle("heading", sample_styles["Heading1"])
	sub_heading = ParagraphStyle("heading", sample_styles["Heading2"])
	
	instructions = """Pease bring this form with you to the UConn Ballroom 
	Dance Club, along with cash or a check made payable to 
	\"UConn Ballroom Dance\" - we do not accept credit cards or huskybucks.  
	The club meets on Monday nights in the Pharmacy Building Lobby 
	at 7 PM"""
	
	if registration.registration_session.first_club_day:
		instructions += " starting on %s." % registration.registration_session.first_club_day.strftime("%B %-d, %Y")
	
	if registration.registration_session.last_free_day:
		instructions += """<br />The first couple weeks of the club are free, 
		until %s.  Payment will be accepted at any time during the semester, but after this 
		date you will not be allowed into the ballroom until your dues 
		have been paid.""" % registration.registration_session.last_free_day.strftime("%B %-d, %Y")
	
	
	if registration.registration_session.early_deadline and registration.registration_session.early_deadline > date.today():
		payment_amount = "Amount due on or before %s: $%0.2f<br />" % (registration.registration_session.early_deadline.strftime("%B %-d, %Y"), registration.amount_due)
		payment_amount += "Amount due after %s: $%0.2f" % (registration.registration_session.early_deadline.strftime("%B %-d, %Y"), (registration.amount_due+registration.registration_session.early_discount))
	else:
		payment_amount = "Amount due: $%0.2f" % registration.amount_due
	
	
	payment_instructions = "Please pay with cash or a check made payable to \"UConn Ballroom Dance\"."
	
	refund_policy = """To recieve a refund, you must return your membership card to a member of our administration.  
	Unless you have extenuating circumstances, refunds will not be granted """
	
	if not registration.registration_session.last_free_day:
		refund_policy += "after the club has been operating for three weeks "
	else:
		refund_policy += "after %s " % registration.registration_session.last_free_day.strftime("%B %-d, %Y") 
	refund_policy += "or one week after you have paid, whichever is later."
	
	barcode = Code128("RF%d" % registration.id, barHeight=144, barWidth=2)
	barcode.quiet = 0
	
	out = StringIO()
	
	doc = SimpleDocTemplate(out, pagesize=(8.5*inch, 11*inch))
	doc.leftMargin = doc.rightMargin = 1*inch
	doc.topMargin = doc.bottomMargin = .5*inch
	
	
	story = [Paragraph("UConn Ballroom Registration Form", title)]
	story.append(Paragraph("Instructions", heading))
	story.append(Paragraph(instructions, normal))
	
	story.append(Spacer(1, .25 * inch))
	
	story.append(Paragraph("Payment", heading))
	story.append(Paragraph(payment_amount, normal))
	story.append(Paragraph(payment_instructions, normal))
	
	story.append(Spacer(1, .25 * inch))
	
	story.append(Paragraph("Refund Policy", heading))
	story.append(Paragraph(refund_policy, normal))
	
	story.append(Spacer(1, .25 * inch))
	
	story.append(Paragraph("Registration Information", heading))
	nameLine = u"Name: %s %s" % (registration.person.first_name, registration.person.last_name)
	
	story.append(Paragraph(nameLine, normal))
	
#	if len(registration.person.email_addressesresses) == 1:
#		story.append(Paragraph("E-Mail Address: %s" % registration.person.email_addresses[0], styles.normal))
#	elif len(reg.person.email_addresses) > 1:
#		story.append(Paragraph("E-Mail Addresses: %s" % ", ".join(map(str, reg.person.email_addresses)), styles.normal))
	
	story.append(Paragraph("Team: %s" % (registration.team and 'Yes' or 'No'), normal))
	story.append(Paragraph("Student Status: %s" % registration.person_type.description, normal))
	story.append(Paragraph("Registration ID: %d" % registration.id, normal))
	story.append(Paragraph("Person ID: %s" % registration.person.id, normal))
	story.append(Spacer(1, .4*inch))
	story.append(Spacer(1, .15*inch))
		
	tableData = [[Spacer(1, 1), barcode, QRCodeFlowable("RF%d" % registration.id, 144, 0), Spacer(1, 1)]]
	innerSize = 8.5*inch - (doc.leftMargin + doc.rightMargin)
	
	story.append(Table(tableData, colWidths=[doc.leftMargin, innerSize-144, 144, doc.rightMargin]))
	story.append(Paragraph(barcode.value, title))
	
	doc.build(story)
	
	return out.getvalue()

def emailChangePayment(registration, oldAmount, newAmount):
	if (oldAmount or 0) == (newAmount or 0):
		return

	change = (newAmount or 0) - (oldAmount or 0)
	if change < 0:
		direction = "Refund"
		change = change * -1
	else:
		direction = "Payment"
		
	teamClub = registration.team and "team and club" or "club"
	
	mailTo = [e.email for e in registration.person.emails.all() if e.send]
	if not mailTo:
		mailTo = ['webmaster@uconnballroom.com']

	subject = "Your UConn Ballroom Receipt for the %s semester" % registration.registration_session
	message = "Your %s of %s has been recorded. You are currently registered as a %s on the %s. Thank you for your continued support of UConn Ballroom." % (direction, change, registration.person_type, teamClub)
	mailFrom = "treasurer@uconnballroom.com"


	for addr in mailTo:
		mailTo = [addr]

		email = EmailMessage(subject, message, mailFrom, mailTo, headers={'X-Person-ID': registration.person.id})
		email.send()
	

def changePaymentAmount(registration, newAmount):
	oldAmount = registration.paid_amount
	
	if newAmount == None:
		registration.paid_amount = None
		registration.paid_date = None
	else:
		if newAmount < 0:
			raise ValueError("Payment amount must be greater than $0.00")
		if not registration.paid_date:
			registration.paid_date = date.today()
			
		registration.paid_amount = newAmount
	
	registration.save()
	emailChangePayment(registration, oldAmount, newAmount)

def registrationCardCodeKey(s):
	year = s[0:2]
	semester = s[2].upper()
	
	remainder = s[3:]
	
	year = int(year)+2000
	return (year, SEMESTERCODES.get(semester, 99999), remainder)
	
	
def codeSearch(s):
	from registration.models import Person, Registration, MembershipCard
	
	searchType = s[0:2].upper()
	searchData = s[2:]
	
	if searchType == 'PE':
		try:
			return Person.objects.get(pk=searchData)
		except Person.DoesNotExist:
			return None
		except ValueError:
			return None
			
	if searchType == "RF":
		try:
			return Registration.objects.get(pk=searchData)
		except Registration.DoesNotExist:
			return None
		except ValueError:
			return None
			
	if searchType == "MC" or searchType == "PC":
		try:
			return MembershipCard.objects.get(membership_card=searchData).registration
		except MembershipCard.DoesNotExist:
			return None
		except ValueError:
			return None
			
	return None
		
def autoPerson(o):
	from registration.models import Person, Registration, MembershipCard, PersonEmail
	
	if isinstance(o, Person):
		return o
	if isinstance(o, Registration):
		return o.person
	if isinstance(o, MembershipCard):
		return o.registration.person
	if isinstance(o, PersonEmail):
		return o.person
	
