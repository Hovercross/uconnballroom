from django.contrib.auth.decorators import permission_required
from decimal import Decimal

from registration.models import RegistrationSession, Registration, Person, MembershipCard

import json

@permission_required("registration.can_manage_payments")
def payment(request):
	pass
	
@permission_required("registration.can_manage_payments")
def changePaidAmount(request):
	data = json.loads(request.raw_post_data)
	
	registration_id = data["registration_id"]
	paid_amount = data["paid_amount"]