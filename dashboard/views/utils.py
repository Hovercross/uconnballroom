from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render

import lists.lib


@permission_required("registraiton.change_persontypeautolist")
def rebuild_managed_lists(request):
	lists.lib.rebuildManagedLists()
	
	return HttpResponse("List rebuild finished")