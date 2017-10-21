from datetime import datetime

from django.shortcuts import render

from django.http import JsonResponse

from compresults.models import Event

# Create your views here.
def projector(request):
    return render(request, "compresults/projector.html")

def projector_json(request):
    events = Event.objects.filter(show=True)

    out = {'events': [], 'last_updated': datetime.now()}

    for event in events:
        assert isinstance(event, Event)

        event_data = {
            'name': event.name
        }

        numbers = event.get_numbers()
        note = event.note

        if numbers:
            event_data['numbers'] = sorted(numbers)

        if note:
            event_data['note'] = note
    
        out['events'].append(event_data)
    
    response = JsonResponse(out)
    return response
