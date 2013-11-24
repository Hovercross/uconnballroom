from django.db import models

import lists.lib

class List(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=50, unique=True)
	
	TYPE_CHOICES = (
		('entry_list', 'Entry List'), 
		('person_type_list', 'Person Type List'), 
		('registration_type_list', 'Club/Team List'), 
		('paid_list', 'Paid Tracking List'),
		('admin_list', 'Administrative List'))
	
	list_type = models.CharField(max_length=254, choices=TYPE_CHOICES)
	
	people = models.ManyToManyField('registration.Person', blank=True)
	
	def __str__(self):
		return self.name
		
class QueryList(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=50, unique=True)
	unrestricted_send = models.BooleanField(default=False)
	query_string = models.TextField()

	@property
	def people(self):
		return lists.lib.parseQueryList(self.query_string, "\n")

	def __str__(self):
		return self.name

