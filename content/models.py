from django import forms
from django.db import models
from django.template.loader import render_to_string

from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.image.models import ImageContent

from biographies.models import BiographySection
from galleries.models import Gallery

Page.register_extensions('feincms.module.page.extensions.navigation', 'feincms.module.extensions.datepublisher', 'feincms.module.page.extensions.titles')

Page.register_templates({
    'title': _('Standard template'),
    'path': 'basic.html',
    'regions': (
        ('main', _('Main content area')),
        ),
    })
			
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

class GalleryContent(models.Model):
	gallery = models.ForeignKey(Gallery)
	
	class Meta:
		abstract = True
		
	def render(self, **kwargs):
		return render_to_string("partial/gallery.html", {'gallery': self.gallery})

#Add content types
Page.create_content_type(RichTextContent)
Page.create_content_type(BiographyContent)
Page.create_content_type(CalendarContent)
Page.create_content_type(ImageContent)
Page.create_content_type(GalleryContent)