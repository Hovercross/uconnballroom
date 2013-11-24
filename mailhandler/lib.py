import email
import logging

from email.MIMEText import MIMEText

from lists.models import QueryList
from mailhandler.models import MailSender

import sys
import traceback
from cStringIO import StringIO

from boto.ses.connection import SESConnection

from django.conf import settings

MAILSYSTEM = "webmaster@uconnballroom.com"

log = logging.getLogger(__name__)

class Message(object):
	keepHeaders = ("Subject", "Date", "From", "To", "Content-Type", "Content-Transfer-Encoding", "Mime-Version", "X-Mailer", "Message-ID")
	authorizedDomains = ("uconnballroom.com", )
	
	def __init__(self, data):
		log.debug("Inititalizing message")
		self.data = str(data)
		self.message = email.message_from_string(str(self.data))
	
	@property
	def spfStatus(self):
		if not self.message.has_key("Received-SPF"):
			return None
		status = self.message["Received-SPF"].split(" ", 1)[0].lower().strip()
		if status == "pass":
			return True
		if status in ('fail', 'softfail'):
			return False
			
		return None
	
	@property
	def deliveryList(self):
		originalTo = self.message["X-Original-To"].lower()
		
		if not originalTo:
			return None
		
		try:	
			localPart, remotePart = originalTo.split("@")
		except ValueError, e:
			log.error("ValueError while splitting %s into user and domain" % originalTo)
			return None
		
		try:
			return QueryList.objects.get(slug=localPart)
		except QueryList.DoesNotExist:
			log.error("Could not find list with slug %s" % localPart)
			return None
	
	@property
	def deliveryPeople(self):
		deliveryList = self.deliveryList
		
		if deliveryList:
			return sorted(deliveryList.people, key=lambda x: (x.sortName))
			
		return None
	
	@property
	def rcptTo(self):
		out = set()
		
		for p in self.deliveryPeople:
			for e in p.emails.filter(send=True):
				out.add(e.email)
				
		return list(out)
	
	@property
	def returnPath(self):
		return email.utils.parseaddr(self.message["return-path"])[1].lower()
	
	@property
	def verifiedSender(self):
		if self.spfStatus == True:
			try:
				return MailSender.objects.get(from_address=self.returnPath)
			except MailSender.DoesNotExist:
				return None
				
		return None		
		
	@property
	def shouldAutoSend(self):
		sender = self.verifiedSender
		deliveryList = self.deliveryList
		
		if sender and sender.unrestricted_send:
			return True
		
		#if deliveryList and deliveryList.unrestricted_send:
		#	return True
			
		return False
				
	def dataToSend(self):
		m = email.message_from_string(self.data)
		verifiedSender = self.verifiedSender
		
		#Remove extra headers
		for header in m.keys():
			if header.lower() not in map(str.lower, Message.keepHeaders):
				del(m[header])
		
		if verifiedSender:
			if verifiedSender.rewrite_from_address:
				del m["return-path"]
				m["return-path"] = verifiedSender.rewrite_from_address
			
			if verifiedSender.rewrite_from_name and verifiedSender.rewrite_from_address:
				del m["from"]
				m["From"] = '"%s " <%s>' % (verifiedSender.rewrite_from_name, verifiedSender.rewrite_from_address)
			elif verifiedSender.rewrite_from_name:
				del m["from"]
				originalAddr = email.utils.parseaddr(m["from"])[1]
				m["From"] = '"%s " <%s>' % (verifiedSender.rewrite_from_name, originalAddr)
			elif verifiedSender.rewrite_from_address:
				del m["from"]
				m["From"] = verifiedSender.rewrite_from_address
		
		return m.as_string()
		
def processMessage(data, forceSend=False):
	log.debug("Message inititliazation started")
	m = Message(data)
	log.debug("Message inititalization complete")
	#Check that there is a delivery list
	if not m.deliveryList:
		log.warn("No delivery list")
		if not m.returnPath:
			log.warn("No return path")
			raise Exception("No return path on e-mail")

		errorMessage = MIMEText("I was unable to find the list you specified.  No e-mail has been sent.")
		errorMessage["To"] = m.returnPath
		errorMessage["From"] = MAILSYSTEM
		errorMessage["Subject"] = "Error sending e-mail"

		if m.spfStatus != False:
			log.info("Sending error message")
			send("webmaster@uconnballroom.com", [m.returnPath], errorMessage.as_string()) 
		else:
			log.info("No SPF status, surpressing error message")
		return

	if len(m.deliveryPeople) == 0:
		log.info("No people on list %s" % m.deliveryList)
		errorMessage = MIMEText("I was able to find the list you specified, but it contains no peoblem.  Your e-mail has not been sent.")
		errorMessage["To"] = m.returnPath
		errorMessage["From"] = MAILSYSTEM
		errorMessage["Subject"] = "Error sending e-mail"

		if m.spfStatus != False:
			log.info("Sending error message")
			send("webmaster@uconnballroom.com", [m.returnPath], errorMessage.as_string())
		else:
			log.info("No SPF status, surpressing error message")
		return

	try:
		if m.shouldAutoSend:
			log.info("Sending list message")
			sendListMessage(m)
		else:
			log.info("Holding list message")
			holdListMessage(m)

	except Exception, e:
		log.error("Processing exception: %s" % e)
		
		exc_type, exc_value, exc_traceback = sys.exc_info()

		lines = traceback.format_tb(exc_traceback)

		errorData = StringIO()
		errorData.write("="*80)
		errorData.write("\n")
		errorData.write("Traceback".center(80, "="))
		errorData.write("\n")
		errorData.write("="*80)
		errorData.write("\n")

		errorData.write("\n")
		errorData.write("".join(lines))
		errorData.write("\n\n")

		errorData.write("="*80)
		errorData.write("\n")
		errorData.write("Exception".center(80, "="))
		errorData.write("\n")
		errorData.write("="*80)
		errorData.write("\n")

		errorData.write(str(e))

		errorData.write("\n\n")
		errorData.write("="*80)
		errorData.write("\n")
		errorData.write("Original Data".center(80, "="))
		errorData.write("\n")
		errorData.write("="*80)
		errorData.write("\n")
		errorData.write(m.dataToSend())
		errorData.write("\n\n")

		#print errorData.getvalue()

		if m.spfStatus != False:
			errorMessage = MIMEText("There was an error sending your e-mail.  The details of the error have been sent to the uconnballroom.com webmaster.")
			errorMessage["To"] = m.returnPath
			errorMessage["From"] = MAILSYSTEM
			errorMessage["Subject"] = "Error sending e-mail"

			send("wembaster@uconnballroom.com", [m.returnPath], errorMessage.as_string())

		tracebackMessage = MIMEText(errorData.getvalue())
		tracebackMessage["From"] = MAILSYSTEM
		tracebackMessage["To"] = "webmaster@uconnballroom.com"
		tracebackMessage["Subject"] = "UConnBallroom.com e-mail list system error"

		

		send("webmaster@uconnballroom.com", ["webmaster@uconnballroom.com"], tracebackMessage.as_string())

def getConfirmationMessage(message):
	people = []
	noRecievers = False

	for p in message.deliveryPeople:
		if p.name:
			people.append(p.name)
		else:
			people.append("Person %d" % p.id)

	if len(people) == 1:
		countStr = "individual: "
	else:
		countStr = "%d people:\n" % len(people)

	if noRecievers:
		noRecieverFootnote = "\n\n*** indicates that the person does not have an e-mail address on file"
	else:
		noRecieverFootnote = ""

	peopleStr = "\n".join(people)
	messageTxt = "Your e-mail with the subject \"%s\" has been sent to the following %s%s%s" % (message.message["subject"], countStr, peopleStr, noRecieverFootnote)

	m = MIMEText(messageTxt)
	m["To"] = message.returnPath
	m["From"] = MAILSYSTEM
	m["Subject"] = "E-Mail delivery report"

	return m

def holdListMessage(m):
	errorMessage = MIMEText("I'm sorry, but the mail system is not currently holding e-mail. Please contact a board member to send your e-mail.")
	errorMessage["To"] = m.returnPath
	errorMessage["From"] = MAILSYSTEM
	errorMessage["Subject"] = "Error sending e-mail"

	if m.spfStatus != False:
		send("webmaster@uconnballroom.com", [m.returnPath], errorMessage.as_string())

	return

def sendListMessage(message):
	confirmMessage = getConfirmationMessage(message)

	for e in message.rcptTo:
		send(None, e, message.dataToSend())

	#send("webmaster@uconnballroom.com", message.rcptTo, message.dataToSend())
	send("webmaster@uconnballroom.com", [message.returnPath], confirmMessage.as_string())

def send(fromAddr, rcptTo, data):
	conn = SESConnection(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
	conn.send_raw_email(data, destinations=rcptTo)
