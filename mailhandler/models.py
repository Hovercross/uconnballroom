from django.db import models

from registration.models import List

class MailSender(models.Model):
	from_address = models.EmailField(max_length=254)
	rewrite_from_name = models.TextField(max_length=200, blank=True)
	rewrite_from_address = models.EmailField(max_length=254, blank=True)
	unrestricted_send = models.BooleanField(default=False)
	send_to_lists = models.ManyToManyField(List, blank=True)
	
	def __str__(self):
		return self.from_address