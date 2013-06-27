from django.contrib import admin
from models import Biography, BiographySection
from adminsortable.admin import SortableTabularInline, SortableAdmin

class BiographyAdmin(SortableAdmin):
    pass

#class BiographyInline(admin.TabularInlineAdmin):
#	model = Biography
#	fields = ['first_name', 'last_name', 'title']
#	readonly_fields = ['first_name', 'last_name', 'title']
	
class BiographySectionAdmin(admin.ModelAdmin):
#	inlines = [BiographyInline]
	pass

admin.site.register(Biography, BiographyAdmin)
admin.site.register(BiographySection, BiographySectionAdmin)