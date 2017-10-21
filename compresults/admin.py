from django.contrib import admin

from adminsortable.admin import SortableAdmin

from compresults.models import Event

class EventAdmin(SortableAdmin):
    list_display = ['__str__', 'show', 'note']
    list_editable = ['show', 'note']

# Register your models here.
admin.site.register(Event, EventAdmin)