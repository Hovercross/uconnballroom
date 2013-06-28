from django.db import models
from adminsortable.models import Sortable
from adminsortable.fields import SortableForeignKey

from easy_thumbnails.files import get_thumbnailer

# Create your models here.

class Gallery(models.Model):
	name = models.CharField(max_length=50)
	
	def __unicode__(self):
		return self.name

class GalleryImage(Sortable):
	image = models.ImageField(upload_to = 'gallery_images')
	title = models.CharField(max_length=50, blank=True, null=True)
	caption = models.TextField(blank=True, null=True)
	gallery = SortableForeignKey(Gallery)
	
	def admin_thumb(self):
		try:
			return '<img src="%s" alt=""/>' % (get_thumbnailer(self.image)['adminThumb'].url)
		except Exception, 2:
			return 'ERROR'
		
	admin_thumb.allow_tags = True
	
	def __unicode__(self):
		if self.title:
			return "%s (%s)" % (self.title, self.image)
		return "%s" % self.id