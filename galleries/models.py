from django.db import models
from adminsortable.models import Sortable
from adminsortable.fields import SortableForeignKey
from django.core.urlresolvers import reverse

from easy_thumbnails.files import get_thumbnailer

# Create your models here.

class Gallery(Sortable):
	name = models.CharField(max_length=50)
	
	def bulk_admin_url(self):
		url = reverse('galleries.views.manage_gallery', args=(self.id, ))
		return '<a href="%s">%s</a>' % (url, url)
	
	bulk_admin_url.allow_tags = True
	
	def __unicode__(self):
		return self.name

class GalleryImage(Sortable):
	image = models.ImageField(upload_to = 'gallery_images')
	title = models.CharField(max_length=50, blank=True, null=True)
	caption = models.TextField(blank=True, null=True)
	gallery = SortableForeignKey(Gallery)
	
	def admin_thumb(self):
		if self.image:
			try:
				return '<img src="%s" alt=""/>' % (get_thumbnailer(self.image)['adminThumb'].url)
			except Exception, e:
				return 'ERROR'
		else:
			return "&nbsp;"
	admin_thumb.allow_tags = True
	
	def __unicode__(self):
		if self.title:
			return "%s (%s)" % (self.title, self.image)
		return "%s" % self.id