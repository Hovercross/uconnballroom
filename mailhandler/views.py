from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json

#from lib import processIncomingMessage

# Create your views here.
@csrf_exempt
def handleIncomingEmail(request):
	if request.method == 'POST':
	    processIncomingMessage(json.loads(request.raw_post_data))
	
	return HttpResponse("OK")