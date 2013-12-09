from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.http import Http404
from django.core.mail import send_mail, EmailMessage

from feincms.module.page.models import Page
from feincms.module.page.extensions.navigation import NavigationExtension, PagePretender

from registration import lib

from django.db import transaction

import json

import logging

logger = logging.getLogger(__name__)

from registration import forms
from registration import models

#Serves the registration form and optionally e-mails it to the user
#TODO: Break the e-mail out elsewhere
def serveRegistrationForm(request, person):
	rs = models.RegistrationSession.objects.get(available=True)
	registration = models.Registration.objects.get(person=person, registration_session=rs)
	registrationForm = lib.getRegistrationForm(registration)
	
	if not registration.sent_registration_email:
		logger.info("Sending registration email to %s" % registration.person)
		with transaction.commit_on_success():
			mailTo = [e.email for e in registration.person.emails.all() if e.send]
			if not mailTo:
				mailTo = ['webmaster@uconnballroom.com']
			
			subject = "Your UConn Ballroom Registration for %s" % rs
			message = "Your UConn Ballroom registration has been complted. Please bring the attached registration form to a meeting of the UConn Ballroom Dance club to process your payment."
			mailFrom = "treasurer@uconnballroom.com"
	
				
			for addr in mailTo:
				mailTo = [addr]
			
				email = EmailMessage(subject, message, mailFrom, mailTo, headers={'X-Person-ID': registration.person.id})
				email.attach('Registration Form.pdf', registrationForm, 'application/pdf')
				email.send()
			
			registration.sent_registration_email = True
			registration.save()
	
	response = HttpResponse(content_type='application/pdf')
	response['Content-Disposition'] = 'filename="registration.pdf"'
	
	response.write(registrationForm)
	return response

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
			
			return serveRegistrationForm(request, email.person)
	
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
		
		with transaction.commit_on_success():
			if 'uconn_email' in form.cleaned_data:
				e = models.PersonEmail(person=person, email=form.cleaned_data["uconn_email"], send=False)
				e.save()
		
			for a in ('first_name', 'last_name', 'gender', 'phone_number', 'hometown', 'netid', 'peoplesoft_number', 'major'):
				if a in form.cleaned_data:
					person_changed = True
					setattr(person, a, form.cleaned_data[a])
				
			for a in ('person_type', 'team'):
				if a in form.cleaned_data:
					registration_changed = True
					setattr(registration, a, form.cleaned_data[a])

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
			return serveRegistrationForm(request, person)
	
	
	#Return nothing if the form wasn't a start or a continue
	return