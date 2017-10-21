from django.contrib import admin

from adminsortable.admin import SortableAdmin

from compresults.models import Event

class NotDoneListFilter(admin.SimpleListFilter):
    title = 'done'
    parameter_name = 'done'

    def lookups(self, request, model_admin):
        return (
            ('done', 'Done'),
            ('notdone', 'Not Done'),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'done':
            return queryset.filter(status='done')
        
        if self.value() == 'notdone':
            return queryset.exclude(status='done')

class EventAdmin(SortableAdmin):
    list_display = ['__str__', 'status']
    list_editable = ['status']

    list_filter = [NotDoneListFilter]

# Register your models here.
admin.site.register(Event, EventAdmin)