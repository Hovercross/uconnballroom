from django.db import models
from django.core.urlresolvers import reverse

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

class RemoteScanEndpoint(models.Model):
    description = models.CharField(max_length=255)
    title = models.CharField(max_length=50)
    auth_key = models.CharField(max_length=40, unique=True)
    allowed_list = models.ForeignKey(QueryList, blank=True, null=True)

    scan_list = models.ForeignKey(List, blank=True, null=True)
    list_prefix = models.CharField(max_length=255, blank=True)
    
    def get_absolute_url(self):
        return reverse("lists_remotescan_setup", kwargs={'id': self.id})
    
    def clean(self):
        if not self.scan_list and not self.list_prefix:
            raise ValidationError('Either Scan list or list_prefix must be set')
        
        elif self.scan_list and self.list_prefix:
            raise ValidationError('Scan list and List prefix may not be set simultainously')
    
    def __str__(self):
        return self.description
        
class RemoteScanUUID(models.Model):
    uuid = models.UUIDField(primary_key=True, editable=False)