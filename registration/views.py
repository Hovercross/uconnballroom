from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from feincms.module.page.models import Page
from feincms.module.page.extensions.navigation import NavigationExtension, PagePretender

from django.db import transaction

import json

import logging

logger = logging.getLogger(__name__)

from . import forms
from . import models

def index(request):
	#Initial request
	if request.method == 'GET':
		logger.debug('Returning empty registration form')
		return 'registration_form.html', {'form': forms.StartForm()}

	#We only handle GET or POST and GET has been handled already
	if request.method != 'POST':
		logger.debug('Raising 404 due to non-post')
		raise Http404
	
	#Handle the start form; all paths return
	if request.POST["form_type"] == "start":
		logger.debug('Handling POSTed start form')
		form = forms.StartForm(request.POST)
		
		#Invalid
		if not form.is_valid():
			logger.debug('Start form not valid')
			return 'registration_form.html', {'form': forms.StartForm(request.POST)}
		
		logger.debug('Falling through to valid start form')
		try:
			email = models.PersonEmail.objects.get(email=form.cleaned_data['email'])
		except models.PersonEmail.DoesNotExist:
			with transaction.commit_on_success():
				person = models.Person()
				person.save()
			
				email = models.PersonEmail(person=person, email=form.cleaned_data['email'])
				email.save()
			
		#Create the continuation form - display it if it's useful, otherwise finish
		#This won't be useful if the person has already registered
		form = forms.ContinueForm(email)	
		if form.useful:
			logger.debug('Form is useful')
			return 'registration_form.html', {'form': form}
		else:
			logger.debug('Form is not useful')
			#TODO: Display the PDF or something
			return "All set!"
	
	#Handle the continuation form; all paths return			
	if request.POST["form_type"] == "continue":
		email = models.PersonEmail.objects.get(email=request.POST['email'])
		
		form = forms.ContinueForm(email, request.POST)
		
		#Re-display the form if invalid
		if not form.is_valid():
			return 'registration_form.html', {'form': forms.ContinueForm(email, request.POST)}
		
		#Save the data
		person = email.person
		rs = models.RegistrationSession.objects.get(available=True)
		try:
			registration = models.Registration.objects.get(person=person, registration_session=rs)
		except models.Registration.DoesNotExist:
			registration = models.Registration(person=person, registration_session=rs)
			
		
		person_changed = False
		registration_changed = False
		
		for a in ('first_name', 'last_name', 'gender', 'phone_number', 'hometown', 'netid', 'peoplesoft_number', 'major'):
			if a in form.cleaned_data:
				person_changed = True
				setattr(person, a, form.cleaned_data[a])
				
		for a in ('person_type', 'team'):
			if a in form.cleaned_data:
				registration_changed = True
				setattr(registration, a, form.cleaned_data[a])

		with transaction.commit_on_success():							
			if person_changed:
				person.save()
			if registration_changed:
				registration.save()
						
		#Create the next iteration of the continuation form
		#Check if it's use and display it if it is. Otherwise finish
		form = forms.ContinueForm(email)
		if form.useful:
			return 'registration_form.html', {'form': form}
		else:
			return "All set!"
	
	
	#Return nothing if the form wasn't a start or a continue
	return
				
	

def required_fields(request):
	email = request.GET.get("email", None)
	
	out = list(forms.registrationRequiredFields(email))
	
	return HttpResponse(json.dumps(out), content_type="application/json")