from django.db import models
from django.template.loader import render_to_string

from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.image.models import ImageContent

from adminsortable.models import Sortable
from adminsortable.fields import SortableForeignKey

from feincms.content.medialibrary.v2 import MediaFileContent

Page.register_extensions('feincms.module.page.extensions.navigation', 'feincms.module.extensions.datepublisher', 'feincms.module.page.extensions.titles')

Page.register_templates({
    'title': _('Standard template'),
    'path': 'basic.html',
    'regions': (
        ('main', _('Main content area')),
        ),
    })

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
			
class BiographyContent(models.Model):
	section = models.ForeignKey(BiographySection)
	
	class Meta:
		abstract = True
		
	def render(self, **kwargs):
		return render_to_string("partial/bio.html", {
			'content': self
		})
		
class CalendarContent(models.Model):
	calendar_src = models.CharField(max_length=200)
	
	class Meta:
		abstract = True
		
	def render(self, **kwargs):
		return render_to_string("partial/calendar.html", {'content': self})

class PositionableImageContent(models.Model):
	CHOICES = (('block', 'Block'), ('left', 'Left'), ('right', 'Right'))
	
	class Meta:
		abstract = True
	
	image = models.ImageField(upload_to='positionable_images')
	relative_to = models.CharField(max_length=10, choices=CHOICES, default='block')
	description = models.CharField(max_length=200)
	horizontal_adjust = models.CharField(max_length=10, blank=True, null=True);
	vertical_adjust = models.CharField(max_length=10, blank=True, null=True);

	@property
	def inlineStyle(self):
		attrs = []

		if self.vertical_adjust:
			attrs.append("margin-top: %s; " % self.vertical_adjust)
			
		if self.relative_to == 'left' and self.horizontal_adjust:
			attrs.append("margin-left: %s;" % self.horizontal_adjust)
		elif self.relatiave_to == 'right' and self.horizontal_adjust:
			attrs.append("margin-right: %s" % self.horizontal_adjust)
			
		print attrs
		if attrs:
			return 'style="%s"' % "; ".join(attrs)
		
			
	def render(self, **kwargs):
		return render_to_string("partial/image.html", {'content': self})

#Add content types
Page.create_content_type(RichTextContent)
Page.create_content_type(BiographyContent)
Page.create_content_type(CalendarContent)
Page.create_content_type(PositionableImageContent)
Page.create_content_type(ImageContent)

Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
        ('default', _('default')),
        ('lightbox', _('lightbox')),
        ))
