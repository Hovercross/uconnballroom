from django.db import models
from adminsortable.models import Sortable
from adminsortable.fields import SortableForeignKey
from django.core.urlresolvers import reverse

import os
import uuid

from easy_thumbnails.files import get_thumbnailer

# Create your models here.

def getGalleryImagePath(instance, fileName):
	prefix, extension = os.path.splitext(fileName)

	if extension:
		uniqueName = "%s%s" % (uuid.uuid4().hex.lower(), extension.lower())
	else:
		uniqueName = uuid.uuid4().hex.lower()
	
	path = os.path.join('gallery_images', str(instance.gallery.id), uniqueName)
	return path
	

class Gallery(Sortable):
	name = models.CharField(max_length=50)
	
	def bulk_admin_url(self):
		url = reverse('galleries.views.manage_gallery', args=(self.id, ))
		return '<a href="%s">%s</a>' % (url, url)
	
	bulk_admin_url.allow_tags = True
	
	def __unicode__(self):
		return self.name

class GalleryImage(Sortable):
	image = models.ImageField(upload_to = getGalleryImagePath)
	title = models.CharField(max_length=50, blank=True, null=True)
	caption = models.TextField(blank=True, null=True)
	gallery = SortableForeignKey(Gallery)
	
	def admin_thumb(self):
		if self.image:
			try:
				return '<img src="%s" alt=""/>' % (get_thumbnailer(self.image)['adminThumb'].url)
			except Exception as e:
				return 'ERROR'
		else:
			return "&nbsp;"
	admin_thumb.allow_tags = True
	
	def __unicode__(self):
		if self.title:
			return "%s (%s)" % (self.title, self.image)
		return "%s" % self.id