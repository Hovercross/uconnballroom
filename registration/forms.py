from django import forms
import logging

from . import models

from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)

class StartForm(forms.Form):
	email = forms.EmailField(label="E-Mail Address")
	form_type = forms.CharField(initial="start", widget=forms.HiddenInput)
	
	def clean_email(self):
		return self.cleaned_data["email"].lower()

class ContinueForm(forms.Form):
	form_type = forms.CharField(initial="continue", widget=forms.HiddenInput)
	
	def __init__(self, email, *args):
		super(ContinueForm, self).__init__(*args)
		rs = models.RegistrationSession.objects.get(available=True)
		person = email.person
		
		self.fields['email'] = forms.CharField(initial=email.email, widget=forms.HiddenInput)
		
		try:
			registration = models.Registration.objects.get(person=person, registration_session=rs)
		except models.Registration.DoesNotExist:
			registration = None
					
		if not person.first_name:
			self.fields['first_name'] = forms.CharField(max_length=200)
		
		if not person.last_name:
			self.fields['last_name'] = forms.CharField(max_length=200)
			
		if not person.gender:
			self.fields['gender'] = forms.ChoiceField(choices = (('M', 'Male'),('F', 'Female')), required=False)
			
		if not registration:
			self.fields['person_type'] = forms.ModelChoiceField(models.PersonType.objects.filter(enabled=True), label="Student Status")
			self.fields['team'] = forms.ChoiceField(choices = ((False, 'No'), (True, 'Yes')), required=False)
		
		if registration:
			if registration.team:
				if not person.phone_number:
					#TODO: Validate
					self.fields['phone_number'] = forms.CharField(max_length=20)
			
			if registration.person_type.uconn_student:
				if not person.peoplesoft_number:
					#TODO: Validate
					self.fields['peoplesoft_number'] = forms.CharField(max_length=10)
					
				if not person.netid:
					#TODO: Validate
					self.fields['netid'] = forms.CharField(max_length=8)
				
				if not person.hometown:
					self.fields['hometown'] = forms.CharField(max_length=100)
					
				if not person.major:
					self.fields['major'] = forms.CharField(max_length=200)
	@property
	def useful(self):
		for f in self.fields:
			logger.debug("Field %s: %s with widget %s" % (f, self.fields[f], self.fields[f].widget))
			if not isinstance(self.fields[f].widget, forms.HiddenInput):
				logger.debug("%s is a useful field" % f)
				return True

		return False