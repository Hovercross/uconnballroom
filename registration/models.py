from django.db import models
from adminsortable.models import Sortable
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.template.defaultfilters import slugify

import unicodedata

# Create your models here.

from datetime import date, datetime

import lib

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

class QueryList(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=50, unique=True)
	unrestricted_send = models.BooleanField(default=False)
	query_string = models.TextField()
	
	@property
	def people(self):
		return lib.parseQueryList(self.query_string, "\n")
		
	def __str__(self):
		return self.name
		
class List(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=50, unique=True)
	unrestricted_send = models.BooleanField(default=False)
	
	TYPE_CHOICES = (
		('entry_list', 'Entry List'), 
		('person_type_list', 'Person Type List'), 
		('registration_type_list', 'Club/Team List'), 
		('paid_list', 'Paid Tracking List'),
		('admin_list', 'Administrative List'))
	
	list_type = models.CharField(max_length=254, choices=TYPE_CHOICES)
	
	included_lists = models.ManyToManyField('self', blank=True, symmetrical=False)
	included_people = models.ManyToManyField(Person, blank=True)
	
	def allPeople(self):
		people = set()
		
		for l in self.allLists():
			people.update(set(l.included_people.all()))
			
		return people
		
	def allLists(self):
		out = set()
		
		self._recursiveLists(out)
		
		return out
		
	def _recursiveLists(self, seenLists):
		if self in seenLists:
			return
			
		seenLists.add(self)
			
		included_lists = set(self.included_lists.all())
		for l in included_lists:
			l._recursiveLists(seenLists)
		
		return
	
	def __str__(self):
		return self.name
	
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
	
	def list_for(self, registrationSession, create=True):
		listName = self.list_name_for(registrationSession)
		
		try:
			return List.objects.get(slug=slugify(listName))
		except List.DoesNotExist:
			if not create:
				return None
				
			o = List()
			o.name = listName
			o.slug = slugify(o.name)
			o.internally_managed=True
			o.save()
			
			return o

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
	
	def updateLists(self):
		addLists = set()
		removeLists = set()
		
		paidList = autoList('%s paid' % self.registration_session.card_code, 'paid_list')
		unpaidList = autoList('%s unpaid' % self.registration_session.card_code, 'paid_list')
		teamList = autoList('%s team' % self.registration_session.card_code, 'person_type_list')
		clubList = autoList('%s club' % self.registration_session.card_code, 'person_type_list')
		
		if self.paid:
			addLists.add(paidList)
			removeLists.add(unpaidList)
		else:
			addLists.add(unpaidList)
			removeLists.add(paidList)
			
		if self.team:
			addLists.add(teamList)
			removeLists.add(clubList)
		else:
			addLists.add(clubList)
			removeLists.add(teamList)
		
		#Get the appropriate lists for the person type of the user
		for apt in PersonTypeAutoList.objects.filter(person_type=self.person_type):
			listName = "%s %s" % (self.registration_session.card_code, apt.list_name)
			addLists.add(autoList(listName, 'person_type_list'))
		
		#Get all the other lists for all the other person types for that registration session, subtracting the lists that the user will now be getting
		#The case of the person's new list will be handled by the fact that they're already in addLists
		for l in (set(List.objects.filter(list_type='person_type_list').filter(name__startswith=self.registration_session.card_code)) - addLists):
			removeLists.add(l)
				
		for l in removeLists:
			if self.person in l.included_people.all():
				print "Removing %s" % l
				l.included_people.remove(self.person)
				l.save()
				
		for l in addLists:
			if self.person not in l.included_people.all():
				print "Adding %s" % l
				l.included_people.add(self.person)
				l.save()
		
	def __str__(self):
		return "Registration %s %s/%s" % (self.id, self.person, self.registration_session)
	
	class Meta:
		unique_together = (('person', 'registration_session'), )
		permissions = (('can_run_reports', 'Can run reports'), ("can_manage_payments", "Can manage payments"))
	
class MembershipCard(models.Model):
	membership_card = models.CharField(max_length=10)
	registration = models.OneToOneField(Registration)
	
def update_lists(sender, instance, **kwargs):
	instance.updateLists()

def autoList(name, type_code):
	slug = slugify(name)
	
	try:
		return List.objects.get(slug=slug)
	except List.DoesNotExist:
		l = List(name=name, slug=slug, list_type=type_code)
		l.save()
		
		return l
	
#Automatically update a registration's lists on it's save
post_save.connect(update_lists, sender=Registration)