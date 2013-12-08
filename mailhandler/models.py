from django.db import models

import tasks

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
		tasks.sendMessage.delay(self.id)
		self.sent = True
		self.save()
	
	def sendHoldMessage(self):
		tasks.sendHoldMessage.delay(self.id)

class MailingListMessageAttachment(models.Model):
	message = models.ForeignKey(MailingListMessage)
	attachment = models.FileField(upload_to='attachments')
	cid = models.CharField(max_length=254, blank=True, null=True)
