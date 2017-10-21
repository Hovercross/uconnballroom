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
    list_per_page = 20

    actions = ['make_hidden', 'make_done', 'make_upcoming']


    def make_hidden(self, request, queryset):
        queryset.update(status='hidden')
    
    make_hidden.short_description = 'Mark selected events as hidden'
    
    def make_done(self, request, queryset):
        queryset.update(status='done')

    make_done.short_description = 'Mark selected events as done'

    def make_upcoming(self, request, queryset):
        queryset.update(status='upcoming')

    make_upcoming.short_description = 'Mark selected events as upcoming'

# Register your models here.
admin.site.register(Event, EventAdmin)