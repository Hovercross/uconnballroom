from django.db import models
from adminsortable.models import Sortable
from django.utils.translation import ugettext_lazy as _
# Create your models here.

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
			return str(self.name)
		elif self.id:
			return "Person %d" % self.id
		else:
			return "Person object"
		
	@property
	def name(self):
		if self.first_name and self.last_name:
			return "%s %s" % (self.first_name, self.last_name)
			
		return None
	
class PersonEmail(models.Model):
	person = models.ForeignKey(Person, related_name="emails")
	email = models.EmailField(max_length=254, unique=True, null=False, blank=False)
	send = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return "E-mail %s %s" % (self.id, self.email)
	
class List(models.Model):
	name = models.CharField(max_length=50, unique=True)
	slug = models.SlugField(max_length=50, unique=True)
	
	included_lists = models.ManyToManyField('self', blank=True)
	included_people = models.ManyToManyField(Person, blank=True)
	
	def __str__(self):
		return self.name
	
class PersonType(Sortable):
	description = models.CharField(max_length=50)
	usg_person_type = models.CharField(max_length=50)
	csc_semester_standing = models.CharField(max_length=50)
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
	team_surcharge = models.DecimalField(max_digits=5, decimal_places=2)
	nonstudent_surcharge = models.DecimalField(max_digits=5, decimal_places=2)
	returning_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True)
	early_discount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	early_deadline = models.DateField(null=True, blank=True)
	
	available = models.BooleanField(default=False)
	
	club_paid_list = models.ForeignKey(List, related_name="+")
	team_paid_list = models.ForeignKey(List, related_name="+")
	club_unpaid_list = models.ForeignKey(List, related_name="+")
	team_unpaid_list = models.ForeignKey(List, related_name="+")
	
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
	

class Registration(models.Model):
	person = models.ForeignKey(Person)
	registration_session = models.ForeignKey(RegistrationSession)
	person_type = models.ForeignKey(PersonType)
	registered_at = models.DateTimeField(auto_now_add=True)
	team = models.BooleanField()
	paid_amount = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	paid_date = models.DateTimeField(null=True)
	sent_registration_email = models.BooleanField(default=False)
	notes = models.TextField(blank=True)
	
	def registration_session_display(self):
		return str(self.registration_session)
		
	def __str__(self):
		return "Registration %s %s/%s" % (self.id, self.person, self.registration_session)
	
	class Meta:
		unique_together = (('person', 'registration_session'), )
	
class MembershipCard(models.Model):
	membership_card = models.CharField(max_length=10)
	registration = models.OneToOneField(Registration)
	
class RegistrationLocator(models.Model):
	code = models.CharField(max_length=10)
	registration = models.OneToOneField(Registration)
	
class MailSender(models.Model):
	from_address = models.EmailField(max_length=254)
	rewrite_from_name = models.TextField(max_length=200, blank=True)
	rewrite_from_address = models.EmailField(max_length=254, blank=True)
	unrestricted_send = models.BooleanField(default=False)
	send_to_lists = models.ManyToManyField(List)