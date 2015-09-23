

import lists.models
import registration.models
from django.db import transaction

from lists.lib import updateListsFor
from celery import shared_task

@shared_task
def rebuildManagedLists():
	with transaction.atomic():
		for l in lists.models.List.objects.filter(list_type__in=['person_type_list', 'registration_type_list', 'paid_list']):
			l.delete()
		
		for r in registration.models.Registration.objects.all():
			updateListsFor(r)