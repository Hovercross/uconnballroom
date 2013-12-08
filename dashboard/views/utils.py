from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

import lists.tasks
import ballroom.celery

@permission_required("registraiton.change_persontypeautolist")
def rebuild_managed_lists(request):
	
	for worker, tasks in ballroom.celery.app.control.inspect().active().items():
		for task in tasks:
			if task["name"] == lists.tasks.rebuildManagedLists.name:
				return HttpResponse("List rebuild is already in progress. Please wait for current task to complete")
	
	lists.tasks.rebuildManagedLists.delay()
	return HttpResponse("List rebuild has been queued.")