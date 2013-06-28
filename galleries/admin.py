from django.contrib import admin

from adminsortable.admin import SortableTabularInline, SortableAdmin
from django.utils.translation import ugettext_lazy as _

from models import Gallery, GalleryImage

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
		
class GalleryAdmin(admin.ModelAdmin):
	pass
	
class GalleryImageAdmin(SortableAdmin):
	list_filter = (GalleryListFilter, )
	list_display = ('admin_thumb', 'title', 'gallery')
	
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryImage, GalleryImageAdmin)