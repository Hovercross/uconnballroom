from django.contrib import admin

import lists.models

class QueryListAdmin(admin.ModelAdmin):
	prepopulated_fields = {'slug': ('name', )}
	fields = ['name', 'slug',  'query_string', 'unrestricted_send', 'showPeople']
	readonly_fields = ('showPeople', )
	
	def showPeople(self, o):
		try:
			people = list(o.people)
		except Exception as e:
			return "Error parsing query list"
			
		people.sort(key=lambda x: (x.last_name, x.first_name))
		
		return ", ".join(map(str, people))
	
	showPeople.short_description = "People"	
	showPeople.allow_tags = True

class ListAdmin(admin.ModelAdmin):
	prepopulated_fields = {"slug": ("name",)}

	filter_horizontal = ('people', )

admin.site.register(lists.models.List, ListAdmin)
admin.site.register(lists.models.QueryList, QueryListAdmin)