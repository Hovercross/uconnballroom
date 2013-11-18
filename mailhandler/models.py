from django.db import models
from django.conf import settings

import email.utils

from webob.multidict import MultiDict

from registration.models import List, Person



import requests

class MailSender(models.Model):
	from_address = models.EmailField(max_length=254)
	rewrite_from_name = models.TextField(max_length=200, blank=True)
	rewrite_from_address = models.EmailField(max_length=254, blank=True)
	unrestricted_send = models.BooleanField(default=False)
	send_to_lists = models.ManyToManyField(List, blank=True)
	
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
	
	people = models.ManyToManyField(Person)
	
	def send(self):
		for person in self.people.all():
			for personEmail in person.emails.filter(send=True):
				data = {}
				data['from'] = email.utils.formataddr((self.from_name, self.from_address)),
				data['to'] = email.utils.formataddr((person.name, personEmail.email))
				data['subject'] = self.subject
				data['text'] = self.body_text
				data['o:tag'] = 'mailing_list_message'

				if self.body_html:
					data['html'] = self.body_html

				attachments = self.mailinglistmessageattachment_set.all()
				postFiles = MultiDict()
			
				for a in attachments:
					if a.cid:
						postFiles.add('inline', (a.cid, a.attachment.read()))
					else:
						postFiles.add('attachment', (a.attachment.name, a.attachment.read()))
				try:		
					r = requests.post('https://api.mailgun.net/v2/test.uconnballroom.com/messages', data=data, files=postFiles, auth=requests.auth.HTTPBasicAuth('api', settings.MAILGUN_KEY))
				except requests.ConnectionError:
					mail_admins("Mailgun error", "Could not connect to Mailgun when sending sending message %d to %s" % (self.id, self.to_address))
			
				if r.status_code != 200:
					mail_admins("Mailgun error", "Error sending message %d to %s: %s" % (self.id, self.to_address, r.text))
				
		self.sent = True
		self.save()
			
	#DKIM signature, SPF

class MailingListMessageAttachment(models.Model):
	message = models.ForeignKey(MailingListMessage)
	attachment = models.FileField(upload_to='attachments')
	cid = models.CharField(max_length=254, blank=True, null=True)