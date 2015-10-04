from django.contrib import admin

from adminsortable.admin import SortableTabularInline, SortableAdmin
from django.utils.translation import ugettext_lazy as _

from galleries.models import Gallery, GalleryImage

from django.forms import TextInput, Textarea
from django.db import models

class GalleryListFilter(admin.SimpleListFilter):
	title = _('gallery')
	parameter_name = 'gallery'
	
	def lookups(self, request, model_admin):
		out = []
		
		for gallery in Gallery.objects.all():
			out.append((str(gallery.id), gallery.name))
			
		return out
	
	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(gallery=self.value())
		return queryset

class GalleryImageInline(SortableTabularInline):
	model = GalleryImage
	
	readonly_fields = ('admin_thumb',)
	
	formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':2, 'cols':40})},
    }
		
class GalleryAdmin(SortableAdmin):
	fields = ['name', 'bulk_admin_url']
	readonly_fields = ('bulk_admin_url', )
	inlines = [GalleryImageInline]
	
class GalleryImageAdmin(SortableAdmin):
	list_filter = (GalleryListFilter, )
	list_display = ('admin_thumb', 'title', 'caption')

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)