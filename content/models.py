from django.db import models
from django.template.loader import render_to_string

#This is crap from FeinCMS that has nowhere better go to
from django.utils.translation import ugettext_lazy as _

from feincms.module.page.models import Page
from feincms.content.richtext.models import RichTextContent
from feincms.content.medialibrary.models import MediaFileContent
from feincms.content.image.models import ImageContent

Page.register_extensions('feincms.module.page.extensions.navigation', 'feincms.module.extensions.datepublisher', 'feincms.module.extensions.translations') # Example set of extensions

Page.register_templates({
    'title': _('Standard template'),
    'path': 'basic.html',
    'regions': (
        ('main', _('Main content area')),
        ),
    })


class BiographyContent(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	title = models.CharField(max_length=50, blank=True, null=True)
	email = models.EmailField(blank=True, null=True)
	biography = models.TextField(blank=True, null=True)
	photo = models.ImageField(upload_to='bio_photos', blank=True, null=True)
	
	class Meta:
		abstract = True
		
	def render(self, **kwargs):
		return render_to_string("partial/bio.html", {
			'content': self
		})

#Add content types
Page.create_content_type(RichTextContent)
Page.create_content_type(BiographyContent)
Page.create_content_type(ImageContent, POSITION_CHOICES=(
    ('left', 'Float to left'),
    ('right', 'Float to right'),
    ('block', 'Block'),
))

Page.create_content_type(MediaFileContent, TYPE_CHOICES=(
    ('default', _('default')),
    ('lightbox', _('lightbox')),
    ))
