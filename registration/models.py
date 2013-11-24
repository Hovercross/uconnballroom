from django.db import models
from adminsortable.models import Sortable
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import slugify

import unicodedata

# Create your models here.

from datetime import date, datetime

class Person(models.Model):
	first_name = models.CharField(max_length=200, blank=True)
	last_name = models.CharField(max_length=200, blank=True)
	gender = models.CharField(max_length=1, choices = (('M', 'Male'),('F', 'Female')), blank=True)
	phone_number = models.CharField(max_length=20, blank=True)
	peoplesoft_number = models.CharField(max_length=10, blank=True)
	netid = models.CharField(max_length=8, blank=True)
	hometown = models.CharField(max_length=100, blank=True)
	major = models.CharField(max_length=200, blank=True)
	notes = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		if self.name:
			return unicodedata.normalize('NFKD', self.name).encode('ascii','ignore')
		elif self.id:
			return "Person %d" % self.id
		else:
			return "Person object"
		
	@property
	def name(self):
		if self.first_name and self.last_name:
			return "%s %s" % (self.first_name, self.last_name)
			
		return None
		
	@property
	def sortName(self):
		if self.first_name and self.last_name:
			return (self.last_name.upper(), self.first_name.upper())
		
		else:
			return (None, )
		
	@property
	def has_uconn_email(self):
		for e in self.emails.all():
			if e.email.lower().endswith("@uconn.edu"):
				return True
				
		return False
		
	
class PersonEmail(models.Model):
	person = models.ForeignKey(Person, related_name="emails")
	email = models.EmailField(max_length=254, unique=True, null=False, blank=False)
	send = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return "E-mail %s %s" % (self.id, self.email)		
	
class PersonType(Sortable):
	description = models.CharField(max_length=50)
	usg_person_type = models.CharField(max_length=50)
	csc_semester_standing = models.CharField(max_length=50, blank=True)
	student_rate = models.BooleanField()
	uconn_student = models.BooleanField()
	enabled = models.BooleanField(default=True)
		
	def __str__(self):
		return u'%s' % self.description

class RegistrationSession(models.Model):
	year = models.IntegerField()
	semester = models.CharField(max_length=10)
	card_code = models.CharField(max_length=4, unique=True)
	base_price = models.DecimalField(max_digits=5, decimal_places=2)
	team_surcharge = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)
	nonstudent_surcharge = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)
	returning_discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)
	early_discount = models.DecimalField(max_digits=5, decimal_places=2, blank=True, default=0)
	early_deadline = models.DateField(null=True, blank=True)
	
	first_club_day = models.DateField(null=True, blank=True)
	last_free_day = models.DateField(null=True, blank=True)
	
	available = models.BooleanField(default=False)
	
	def save(self, *args, **kwargs):
		if self.available:
			q = RegistrationSession.objects.filter(available=True)
			
			for previouslyAvailable in q:
				if previouslyAvailable == self:
					continue
				
				previouslyAvailable.available = False
				previouslyAvailable.save()
				
		super(RegistrationSession, self).save(*args, **kwargs)
			
	def __str__(self):
		return "%s %s" % (self.year, self.semester)
	

class PersonTypeAutoList(models.Model):
	person_type = models.ForeignKey(PersonType)
	list_name = models.CharField(max_length=50)
	
	def list_name_for(self, registrationSession):
		return "%s-%s" % (registrationSession.card_code.upper(), self.list_name)

class Registration(models.Model):
	person = models.ForeignKey(Person)
	registration_session = models.ForeignKey(RegistrationSession)
	person_type = models.ForeignKey(PersonType)
	registered_at = models.DateTimeField(auto_now_add=True)
	team = models.BooleanField()
	paid_amount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	paid_date = models.DateTimeField(null=True, blank=True)
	sent_registration_email = models.BooleanField(default=False)
	notes = models.TextField(blank=True)
	
	def registration_session_display(self):
		return str(self.registration_session)
	
	@property
	def amount_charged(self):
		amount = self.registration_session.base_price
			
		if self.team:
			amount += self.registration_session.team_surcharge
		
		if not self.person_type.student_rate:
			amount += self.registration_session.nonstudent_surcharge
			
		if self.registration_session.early_deadline and self.registration_session.early_deadline >= self.effectiveDateCharged:
			amount -= self.registration_session.early_discount
			
		return amount
	
	@property
	def effectiveDateCharged(self):
		if self.paid_date:
			return self.paid_date.date()
		return date.today()
	
	@property
	def amount_due(self):
		if self.paid_amount:
			return self.amount_charged - self.paid_amount
		return self.amount_charged
	
	
	@property
	def paid(self):
		if self.paid_amount == None:
			return False
		
		return True
		
	def __str__(self):
		return "Registration %s %s/%s" % (self.id, self.person, self.registration_session)
	
	class Meta:
		unique_together = (('person', 'registration_session'), )
		permissions = (
			('can_run_reports', 'Can run reports'), 
			("can_manage_payments", "Can manage payments"), 
			("can_autocomplete", "Can use autocomplete"),
			("entry_tracker", "Can use entry tracker"),
			
			)
	
class MembershipCard(models.Model):
	membership_card = models.CharField(max_length=10)
	registration = models.OneToOneField(Registration)