from django.db import models

from adminsortable.models import Sortable
from adminsortable.fields import SortableForeignKey


# Create your models here.

class BiographySection(models.Model):
	title = models.CharField(max_length = 50)

	def __str__(self):
		return self.title

class Biography(Sortable):
	class Meta(Sortable.Meta):
	    pass

	section = SortableForeignKey(BiographySection)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	title = models.CharField(max_length=50, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	biography = models.TextField(blank=True, null=True)
	photo = models.ImageField(upload_to='bio_photos', blank=True, null=True)
	
	def __unicode__(self):
		if self.title:
			return "%s (%s %s)" % (self.title, self.first_name, self.last_name)
		else:
			return "%s %s" % (self.first_name, self.last_name)