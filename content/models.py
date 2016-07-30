from django import forms
from django.db import models
from django.template.loader import render_to_string

from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.application.models import ApplicationContent

from biographies.models import BiographySection

from mptt.fields import TreeForeignKey

from feincms.content.application.models import app_reverse

import uuid
import os

from django.core.exceptions import ImproperlyConfigured

from feincms import settings
from feincms.templatetags import feincms_thumbnail

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


class SubtitledHeader(models.Model):
	heading = models.CharField(max_length=100)
	subtitle = models.CharField(max_length=200)
	
	class Meta:
		abstract = True
		
	def render(self, **kwargs):
		return render_to_string("partial/subtitledHeader.html", {'content': self})


#Moved out of class definitation for Django 1.7 migrations
def getUploadTo(instance, originalPath):
	prefix, extension = os.path.splitext(originalPath)
	uniqueName = "%s%s" % (uuid.uuid4().hex, extension)
	return os.path.join(settings.FEINCMS_UPLOAD_PREFIX, 'imagecontent', uniqueName)


#Straight copy-pasta from the FeinCMS ImageContent so that I can override the upload_to parameter
#Inheritance wasn't working for me, since Django wouldn't let me override the existing image field
class ImageContent(models.Model):
    # You should probably use
    # `feincms.content.medialibrary.models.MediaFileContent` instead.

    """
    Create an ImageContent like this::

        Cls.create_content_type(
            ImageContent,
            POSITION_CHOICES=(
                ('left', 'Float to left'),
                ('right', 'Float to right'),
                ('block', 'Block'),
            ),
            FORMAT_CHOICES=(
                ('noop', 'Do not resize'),
                ('cropscale:100x100', 'Square Thumbnail'),
                ('cropscale:200x450', 'Medium Portait'),
                ('thumbnail:1000x1000', 'Large'),
            ))

        Note that FORMAT_CHOICES is optional. The part before the colon
        corresponds to the template filters in the ``feincms_thumbnail``
        template filter library. Known values are ``cropscale`` and
        ``thumbnail``. Everything else (such as ``noop``) is ignored.
    """
    
    image = models.ImageField(
        _('image'), max_length=255,
        upload_to=getUploadTo)
    alt_text = models.CharField(
        _('alternate text'), max_length=255, blank=True,
        help_text=_('Description of image'))
    caption = models.CharField(_('caption'), max_length=255, blank=True)

    class Meta:
        abstract = True
        verbose_name = _('image')
        verbose_name_plural = _('images')

    def render(self, **kwargs):
        templates = ['content/image/default.html']
        if hasattr(self, 'position'):
            templates.insert(0, 'content/image/%s.html' % self.position)
        return render_to_string(
            templates,
            {'content': self},
            context_instance=kwargs.get('context'))

    def get_image(self):
        type, separator, size = getattr(self, 'format', '').partition(':')
        if not size:
            return self.image

        thumbnailer = {
            'cropscale': feincms_thumbnail.CropscaleThumbnailer,
            }.get(type, feincms_thumbnail.Thumbnailer)
        return thumbnailer(self.image, size)

    @classmethod
    def initialize_type(cls, POSITION_CHOICES=None, FORMAT_CHOICES=None):
        if POSITION_CHOICES:
            models.CharField(
                _('position'),
                max_length=10,
                choices=POSITION_CHOICES,
                default=POSITION_CHOICES[0][0]
                ).contribute_to_class(cls, 'position')

        if FORMAT_CHOICES:
            models.CharField(
                _('format'),
                max_length=64,
                choices=FORMAT_CHOICES,
                default=FORMAT_CHOICES[0][0]
                ).contribute_to_class(cls, 'format')
	
#Add content types
Page.create_content_type(RichTextContent)
Page.create_content_type(BiographyContent)
Page.create_content_type(CalendarContent)
Page.create_content_type(ImageContent, POSITION_CHOICES=(
        ('left', 'Float to left'),
        ('right', 'Float to right'),
        ('block', 'Block'),
    ),)
Page.create_content_type(SubtitledHeader)
Page.create_content_type(ApplicationContent, APPLICATIONS=(
    ('registration.urls', 'Registration application'),
    ))