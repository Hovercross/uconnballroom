# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import feincms.contrib.fields
import feincms.module.extensions.datepublisher
import feincms.module.mixins
import feincms.contrib.richtext
import mptt.fields
import content.models
import feincms.extensions


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0001_initial'),
        ('biographies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationContent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('parameters', feincms.contrib.fields.JSONField(null=True, editable=False)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('urlconf_path', models.CharField(verbose_name='application', choices=[('registration.urls', 'Registration application')], max_length=100)),
            ],
            options={
                'permissions': [],
                'verbose_name_plural': 'application contents',
                'abstract': False,
                'db_table': 'page_page_applicationcontent',
                'verbose_name': 'application content',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='BiographyContent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
            ],
            options={
                'permissions': [],
                'verbose_name_plural': 'biography contents',
                'abstract': False,
                'db_table': 'page_page_biographycontent',
                'verbose_name': 'biography content',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='CalendarContent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('calendar_src', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
            ],
            options={
                'permissions': [],
                'verbose_name_plural': 'calendar contents',
                'abstract': False,
                'db_table': 'page_page_calendarcontent',
                'verbose_name': 'calendar content',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='GalleryContent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('gallery', models.ForeignKey(to='galleries.Gallery')),
            ],
            options={
                'permissions': [],
                'verbose_name_plural': 'gallery contents',
                'abstract': False,
                'db_table': 'page_page_gallerycontent',
                'verbose_name': 'gallery content',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='ImageContent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('image', models.ImageField(verbose_name='image', max_length=255, upload_to=content.models.getUploadTo)),
                ('alt_text', models.CharField(verbose_name='alternate text', max_length=255, blank=True, help_text='Description of image')),
                ('caption', models.CharField(verbose_name='caption', max_length=255, blank=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('position', models.CharField(default='left', verbose_name='position', choices=[('left', 'Float to left'), ('right', 'Float to right'), ('block', 'Block')], max_length=10)),
            ],
            options={
                'permissions': [],
                'verbose_name_plural': 'images',
                'abstract': False,
                'db_table': 'page_page_imagecontent',
                'verbose_name': 'image',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('title', models.CharField(verbose_name='title', max_length=200, help_text='This title is also used for navigation menu items.')),
                ('slug', models.SlugField(verbose_name='slug', max_length=150, help_text='This is used to build the URL for this page')),
                ('in_navigation', models.BooleanField(default=False, verbose_name='in navigation')),
                ('override_url', models.CharField(verbose_name='override URL', max_length=255, blank=True, help_text="Override the target URL. Be sure to include slashes at the beginning and at the end if it is a local URL. This affects both the navigation and subpages' URLs.")),
                ('redirect_to', models.CharField(verbose_name='redirect to', max_length=255, blank=True, help_text='Target URL for automatic redirects or the primary key of a page.')),
                ('_cached_url', models.CharField(default='', editable=False, blank=True, verbose_name='Cached URL', db_index=True, max_length=255)),
                ('lft', models.PositiveIntegerField(db_index=True, editable=False)),
                ('rght', models.PositiveIntegerField(db_index=True, editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(db_index=True, editable=False)),
                ('navigation_extension', models.CharField(null=True, help_text='Select the module providing subpages for this page if you need to customize the navigation.', verbose_name='navigation extension', blank=True, max_length=200)),
                ('publication_date', models.DateTimeField(default=feincms.module.extensions.datepublisher.granular_now, verbose_name='publication date')),
                ('publication_end_date', models.DateTimeField(null=True, verbose_name='publication end date', blank=True, help_text='Leave empty if the entry should stay active forever.')),
                ('_content_title', models.TextField(verbose_name='content title', blank=True, help_text='The first line is the main title, the following lines are subtitles.')),
                ('_page_title', models.CharField(verbose_name='page title', max_length=69, blank=True, help_text='Page title for browser window. Same as title by default. Must be 69 characters or fewer.')),
                ('template_key', models.CharField(default='basic.html', verbose_name='template', choices=[('basic.html', 'Standard template')], max_length=255)),
                ('parent', models.ForeignKey(to='page.Page', null=True, blank=True, verbose_name='Parent', related_name='children')),
            ],
            options={
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
                'ordering': ['tree_id', 'lft'],
            },
            bases=(models.Model, feincms.extensions.ExtensionsMixin, feincms.module.mixins.ContentModelMixin),
        ),
        migrations.CreateModel(
            name='PhotoLink',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('image', models.ImageField(upload_to='gallery_link_photos')),
                ('alt', models.CharField(max_length=200)),
                ('caption', models.CharField(max_length=30, blank=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('page', mptt.fields.TreeForeignKey(to='page.Page', related_name='link_to')),
                ('parent', models.ForeignKey(to='page.Page', related_name='photolink_set')),
            ],
            options={
                'permissions': [],
                'verbose_name_plural': 'photo links',
                'abstract': False,
                'db_table': 'page_page_photolink',
                'verbose_name': 'photo link',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='RichTextContent',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('text', feincms.contrib.richtext.RichTextField(verbose_name='text', blank=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(to='page.Page', related_name='richtextcontent_set')),
            ],
            options={
                'permissions': [],
                'verbose_name_plural': 'rich texts',
                'abstract': False,
                'db_table': 'page_page_richtextcontent',
                'verbose_name': 'rich text',
                'ordering': ['ordering'],
            },
        ),
        migrations.CreateModel(
            name='SubtitledHeader',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('heading', models.CharField(max_length=100)),
                ('subtitle', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(to='page.Page', related_name='subtitledheader_set')),
            ],
            options={
                'permissions': [],
                'verbose_name_plural': 'subtitled headers',
                'abstract': False,
                'db_table': 'page_page_subtitledheader',
                'verbose_name': 'subtitled header',
                'ordering': ['ordering'],
            },
        ),
        migrations.AddField(
            model_name='imagecontent',
            name='parent',
            field=models.ForeignKey(to='page.Page', related_name='imagecontent_set'),
        ),
        migrations.AddField(
            model_name='gallerycontent',
            name='parent',
            field=models.ForeignKey(to='page.Page', related_name='gallerycontent_set'),
        ),
        migrations.AddField(
            model_name='calendarcontent',
            name='parent',
            field=models.ForeignKey(to='page.Page', related_name='calendarcontent_set'),
        ),
        migrations.AddField(
            model_name='biographycontent',
            name='parent',
            field=models.ForeignKey(to='page.Page', related_name='biographycontent_set'),
        ),
        migrations.AddField(
            model_name='biographycontent',
            name='section',
            field=models.ForeignKey(to='biographies.BiographySection'),
        ),
        migrations.AddField(
            model_name='applicationcontent',
            name='parent',
            field=models.ForeignKey(to='page.Page', related_name='applicationcontent_set'),
        ),
    ]
