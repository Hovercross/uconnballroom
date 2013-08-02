from django import forms
from django.db import models
from django.template.loader import render_to_string

from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.image.models import ImageContent

from biographies.models import BiographySection
from galleries.models import Gallery

from mptt.fields import TreeForeignKey

from feincms.content.application.models import app_reverse

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
	
	@property
	def media(self):
		return forms.Media(
			js=('/static/js/jquery.min.js','/static/lightbox/js/lightbox-2.6.min.js'),
			css={'all': ('/static/lightbox/css/lightbox.css', )}
		)
	
	class Meta:
		abstract = True
		
	def render(self, **kwargs):
		return render_to_string("partial/gallery.html", {'gallery': self.gallery})

class PhotoLink(models.Model):
	image = models.ImageField(upload_to='gallery_link_photos')
	alt = models.CharField(max_length=200)
	page = TreeForeignKey(Page, related_name='link_to')
	caption = models.CharField(max_length=30, blank=True)
	
	@property
	def href(self):
		return self.page.get_absolute_url()
	
	class Meta:
		abstract = True
		
	def render(self, **kwargs):
		return render_to_string("partial/galleryLink.html", {'content': self})

class SubtitledHeader(models.Model):
	heading = models.CharField(max_length=100)
	subtitle = models.CharField(max_length=200)
	
	class Meta:
		abstract = True
		
	def render(self, **kwargs):
		return render_to_string("partial/subtitledHeader.html", {'content': self})

#Add content types
Page.create_content_type(RichTextContent)
Page.create_content_type(BiographyContent)
Page.create_content_type(CalendarContent)
Page.create_content_type(ImageContent, POSITION_CHOICES=(
        ('left', 'Float to left'),
        ('right', 'Float to right'),
        ('block', 'Block'),
    ),)
Page.create_content_type(GalleryContent)
Page.create_content_type(SubtitledHeader)
Page.create_content_type(PhotoLink)