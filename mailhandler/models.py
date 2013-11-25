from django.db import models
from django.conf import settings

from webob.multidict import MultiDict
from cStringIO import StringIO
import email.utils
import requests
import os

class MailSender(models.Model):
	from_address = models.EmailField(max_length=254)
	rewrite_from_name = models.TextField(max_length=200, blank=True)
	rewrite_from_address = models.EmailField(max_length=254, blank=True)
	unrestricted_send = models.BooleanField(default=False)
	send_to_lists = models.ManyToManyField('lists.List', blank=True)
	
	def __str__(self):
		return self.from_address
		
class MailingListMessage(models.Model):
	from_address = models.EmailField(max_length=254)
	from_name = models.CharField(max_length=254)
	return_path = models.EmailField(max_length=254)
	subject = models.TextField()
	incoming_message_id = models.CharField(max_length=254)
	body_text = models.TextField()
	body_html = models.TextField()
	sent = models.BooleanField(default=False)
	message_id = models.CharField(max_length=254, blank=True)
	
	people = models.ManyToManyField('registration.Person')
	
	def send(self):
		for person in self.people.all():
			for personEmail in person.emails.filter(send=True):
				data = {}
				data['from'] = email.utils.formataddr((self.from_name, self.from_address)),
				data['to'] = email.utils.formataddr((person.name, personEmail.email))
				data['subject'] = self.subject
				data['text'] = self.body_text
				data['o:tag'] = 'mailing_list_message'
				
				if self.message_id:
					data['h:Message-Id'] = self.message_id
					
				if self.body_html:
					data['html'] = self.body_html

				attachments = self.mailinglistmessageattachment_set.all()
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
					r = requests.post('https://api.mailgun.net/v2/lists.uconnballroom.com/messages', data=data, files=postFiles, auth=requests.auth.HTTPBasicAuth('api', settings.MAILGUN_KEY))
				except requests.ConnectionError:
					mail_admins("Mailgun error", "Could not connect to Mailgun when sending sending message %d to %s" % (self.id, self.to_address))
			
				if r.status_code != 200:
					mail_admins("Mailgun error", "Error sending message %d to %s: %s" % (self.id, self.to_address, r.text))
		
		self.sendConfirmationMessage()		
		self.sent = True
		self.save()
	
	def sendConfirmationMessage(self):
		people = self.people.filter(emails__send=True).distinct()
		
		out = StringIO()
		out.write('Your e-mail with the subject "%s" has been sent to the following %d individual(s):\n' % (self.subject, people.count()))
		for p in people.all():
			if p.name:
				out.write(p.name)
			else:
				out.write("Name less person %d" % p.id)
			out.write("\n")

		out.write("\n")
		out.write("Auxillary message information:\n")
		out.write("Internal message ID: %d\n" % self.id)
		
		data = {}
		data['from'] = email.utils.formataddr(("UConn Ballroom E-mail System", "webmaster@uconnballroom.com")),
		data['to'] = email.utils.formataddr((self.from_name, self.from_address))
		data['subject'] = "E-Mail Delivery Report"
		data['text'] = out.getvalue()
		
		try:		
			r = requests.post('https://api.mailgun.net/v2/uconnballroom.com/messages', data=data, auth=requests.auth.HTTPBasicAuth('api', settings.MAILGUN_KEY))
		except requests.ConnectionError:
			mail_admins("Mailgun error", "Could not connect to Mailgun when sending sending message %d to %s" % (self.id, self.to_address))
		
	def sendHoldMessage(self):
		data = {}
		data['from'] = email.utils.formataddr(("UConn Ballroom E-mail System", "webmaster@uconnballroom.com")),
		data['to'] = email.utils.formataddr((self.from_name, self.from_address))
		data['subject'] = 'Your e-mail with the subject "%s" has been queued' % self.subject
		
		data['text'] = "Your e-mail has been queued for review by an administrator.  You will get an e-mail once it has been sent.  You may reply to this e-mail if you have any questions."
		
		try:		
			r = requests.post('https://api.mailgun.net/v2/uconnballroom.com/messages', data=data, auth=requests.auth.HTTPBasicAuth('api', settings.MAILGUN_KEY))
		except requests.ConnectionError:
			mail_admins("Mailgun error", "Could not connect to Mailgun when sending sending message %d to %s" % (self.id, self.to_address))

class MailingListMessageAttachment(models.Model):
	message = models.ForeignKey(MailingListMessage)
	attachment = models.FileField(upload_to='attachments')
	cid = models.CharField(max_length=254, blank=True, null=True)
