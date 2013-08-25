from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.units import inch
from reportlab.graphics.barcode.code128 import Code128

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from datetime import date

from qr import QRCodeFlowable

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
	The club meets on Monday nights in the UConn Student Union Ballroom 
	(Room 330/331) at 7 PM"""
	
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
	
#	if len(registration.person.email_addresses) == 1:
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
	
	