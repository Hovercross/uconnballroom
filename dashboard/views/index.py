from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from registration.models import QueryList

from datetime import datetime

@login_required
def index(request):
	templateVars = {}
	templateVars["default_club_entry_list"] = "Entry %s" % datetime.today().strftime("%Y-%m-%d")
	templateVars["query_lists"] = QueryList.objects.all().order_by('slug')
	
	return render(request, "dashboard_index.html", templateVars)
