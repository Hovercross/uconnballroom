

from mailhandler import models

from celery import shared_task

from django.conf import settings

from webob.multidict import MultiDict
from io import StringIO
import email.utils
import requests

@shared_task
def sendMessage(id):
	m = models.MailingListMessage.objects.get(pk=id)
	
	for person in m.people.all():
		for personEmail in person.emails.filter(send=True):
			data = {}
			data['from'] = email.utils.formataddr((m.from_name, m.from_address)),
			data['to'] = email.utils.formataddr((person.name, personEmail.email))
			data['subject'] = m.subject
			data['text'] = m.body_text
			data['o:tag'] = 'mailing_list_message'
			
			if m.message_id:
				data['h:Message-Id'] = m.message_id
				
			if m.body_html:
				data['html'] = m.body_html

			attachments = m.mailinglistmessageattachment_set.all()
			postFiles = MultiDict()
		
			for a in attachments:
				if a.cid:
					originalName, originalExt = os.path.splitext(a.attachment.name)
					newName = "%s%s" % (a.cid, originalExt)
					data['html'] = data['html'].replace(a.cid, newName)
					
					postFiles.add('inline', (newName, a.attachment.read()))
				else:
					postFiles.add('attachment', (a.attachment.name, a.attachment.read()))
			try:		
				r = requests.post('https://api.mailgun.net/v2/uconnballroom.com/messages', data=data, files=postFiles, auth=requests.auth.HTTPBasicAuth('api', settings.MAILGUN_KEY))
			except requests.ConnectionError:
				mail_admins("Mailgun error", "Could not connect to Mailgun when sending sending message %d to %s" % (m.id, m.to_address))
		
			if r.status_code != 200:
				mail_admins("Mailgun error", "Error sending message %d to %s: %s" % (m.id, m.to_address, r.text))
	
	sendConfirmationMessage.delay(id)
	
@shared_task
def sendConfirmationMessage(id):
	m = models.MailingListMessage.objects.get(pk=id)
	
	people = m.people.filter(emails__send=True).distinct()

	out = StringIO()
	out.write('Your e-mail with the subject "%s" has been sent to the following %d individual(s):\n' % (m.subject, people.count()))
	for p in people.all():
		if p.name:
			out.write(p.name)
		else:
			out.write("Name less person %d" % p.id)
		out.write("\n")

	out.write("\n")
	out.write("Auxillary message information:\n")
	out.write("Internal message ID: %d\n" % m.id)

	data = {}
	data['from'] = email.utils.formataddr(("UConn Ballroom E-mail System", "mailhandler@lists.uconnballroom.com")),
	data['to'] = email.utils.formataddr((m.from_name, m.from_address))
	data['subject'] = "E-Mail Delivery Report"
	data['text'] = out.getvalue()
	data['h:Reply-To'] = "webmaster@uconnballroom.com"
	
	try:		
		r = requests.post('https://api.mailgun.net/v2/lists.uconnballroom.com/messages', data=data, auth=requests.auth.HTTPBasicAuth('api', settings.MAILGUN_KEY))
	except requests.ConnectionError:
		mail_admins("Mailgun error", "Could not connect to Mailgun when sending sending message %d to %s" % (m.id, m.to_address))

@shared_task
def sendHoldMessage(id):
	m = models.MailingListMessage.objects.get(pk=id)
	
	data = {}
	data['from'] = email.utils.formataddr(("UConn Ballroom E-mail System", "mailhandler@lists.uconnballroom.com")),
	data['to'] = email.utils.formataddr((m.from_name, m.from_address))
	data['subject'] = 'Your e-mail with the subject "%s" has been queued' % m.subject

	data['text'] = "Your e-mail has been queued for review by an administrator.  You will get an e-mail once it has been sent.  You may reply to this e-mail if you have any questions."
	data['h:Reply-To'] = "board@uconnballroom.com"
	
	try:		
		r = requests.post('https://api.mailgun.net/v2/lists.uconnballroom.com/messages', data=data, auth=requests.auth.HTTPBasicAuth('api', settings.MAILGUN_KEY))
	except requests.ConnectionError:
		mail_admins("Mailgun error", "Could not connect to Mailgun when sending sending message %d to %s" % (m.id, m.to_address))
