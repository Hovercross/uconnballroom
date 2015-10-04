from django.contrib import admin
from adminsortable.admin import SortableTabularInline, SortableAdmin

from biographies.models import Biography, BiographySection

class BiographyAdmin(SortableAdmin):
    pass

class BiographySectionAdmin(admin.ModelAdmin):
	pass
	
admin.site.register(Biography, BiographyAdmin)
admin.site.register(BiographySection, BiographySectionAdmin)
