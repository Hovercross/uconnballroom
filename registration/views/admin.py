from django.contrib.auth.decorators import permission_required
from django.db import transaction
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import redirect

from decimal import Decimal

from registration.models import RegistrationSession, Registration, Person, MembershipCard
from registration.lib import changePaymentAmount

import json

@permission_required("registration.can_manage_payments")
def payment(request):
	if 'currentForm' not in request.REQUEST:
		rs = RegistrationSession.objects.get(available=True)
		registrations = Registration.objects.filter(registration_session=rs)
	
		data = []
	
		for r in registrations:
			emails = [e.email for e in r.person.emails.all()]
			emailsStr = ", ".join(emails)
		
			data.append(("%s %s (%s)" % (r.person.first_name, r.person.last_name, emailsStr), r.id))
	
		return 'admin/search.html', {'searchData': data}
	elif request.method == 'GET' and request.GET["currentForm"] == 'search':
		scanType = request.GET["scan"][0:2].upper()
		scanData = request.GET["scan"][2:]
		
		if scanType == "RF":
			registration = Registration.objects.get(pk=scanData)
			if not registration.registration_session.available:
				raise ValueError ("Old registration session called up")
		elif scanType == "MC" or scanType == "PC":
			registration = MembershipCard.objects.get(membership_card=scanData).registration
		
		if registration.paid_amount == None:
			payField = registration.amount_due
		else:
			payField = registration.paid_amount
		
		try:
			mc = "PC%s" % MembershipCard.objects.get(registration=registration).membership_card
		except MembershipCard.DoesNotExist:
			mc = ""
		
		return 'admin/payment.html', {'registration': registration, 'teamDisp': (registration.team and "Yes" or "No"), 'payField': payField, 'membershipCard': mc}
		
	elif request.method == 'POST' and request.POST["currentForm"] == "payment":
		if not request.POST["membership_card"]:
			membershipCard = None
		else:
			if request.POST["membership_card"][0:2].upper() not in ("MC", "PC"):
				raise ValueError("Non-membership card in a membership card field")
			membershipCard = request.POST["membership_card"][2:].upper()
		
		if request.POST["payment_amount"] == "":
			paymentAmount = None
		else:
			paymentAmount = Decimal(request.POST["payment_amount"])
			
		registration = Registration.objects.get(pk=request.POST["registration_id"])
		
		with transaction.atomic():
			for mc in MembershipCard.objects.filter(membership_card=membershipCard):
				mc.delete()
			
			if membershipCard:
				mc = MembershipCard(membership_card=membershipCard, registration=registration)
				registration.membership_card = mc
				mc.save()
			else:
				for mc in MembershipCard.objects.filter(membership_card=membershipCard):
					mc.delete()
			
			changePaymentAmount(registration, paymentAmount)
			
		return redirect('/registration/payment/')
			
