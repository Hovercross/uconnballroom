from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum

from lists.models import QueryList
import registration.models

from datetime import datetime

@login_required
def index(request):
	registration_session = registration.models.RegistrationSession.objects.get(available=True)
	registrations = registration.models.Registration.objects.filter(registration_session=registration_session)
	
	teamPaid = registrations.filter(team=True, paid_amount__isnull=False).count()
	clubPaid = registrations.filter(team=False, paid_amount__isnull=False).count()
	
	teamUnpaid = registrations.filter(team=True, paid_amount__isnull=True).count()
	clubUnpaid = registrations.filter(team=False, paid_amount__isnull=True).count()
	
	totalDollars = registrations.aggregate(Sum('paid_amount'))["paid_amount__sum"]
	
	templateVars = {
		'team_paid': teamPaid,
		'club_paid': clubPaid,
		'team_unpaid': teamUnpaid,
		'club_unpaid': clubUnpaid,
		'total_paid': totalDollars
	}
	
	return render(request, "dashboard_index.html", templateVars)
