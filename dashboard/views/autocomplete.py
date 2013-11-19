from django.http import HttpResponse
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

from registration.models import Person, RegistrationSession

import json

def autocompleteQuery(searchArgs, inSession=None):
	q = Q()
	
	if inSession:
		q = Q(registration__registration__session__in=inSession)
	
	for token in searchArgs:
		tokenSearch = Q(first_name__icontains=token) | Q(last_name__icontains=token) | Q(emails__email__icontains=token)
		if q == None:
			q = tokenSearch
		else:
			q = q & tokenSearch
			
	return Person.objects.filter(q).distinct()
	
@permission_required('registration.can_autocomplete')
def search(request):
	searchQ = request.GET.get("term", None)
	sessionsQ = request.GET.getlist("session", None)

	if not searchQ:
		return []

	#Get the base person query	
	query = autocompleteQuery(searchQ.split(" "))

	#Add on the registration session filter
	if sessionsQ:
		sessions = RegistrationSession.objects.filter(card_code__in=sessionsQ)

		query = query.filter(registration__registration_session__in=sessions)

	#Grab emails - not done above to limit the table scan of emails
	query = query.prefetch_related('emails')

	out = []

	for person in query:
		out.append({'id': person.id, 'first_name': person.first_name, 'last_name': person.last_name, 'emails': [e.email for e in person.emails.all()]})

	response = HttpResponse(content_type="application/json")
	json.dump(out, response)
	return response