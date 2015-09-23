# -*- coding: utf-8 -*-


from django.db import models, migrations
import feincms.module.extensions.datepublisher
import feincms.contrib.fields
import feincms.contrib.richtext
import feincms.extensions
import content.models
import mptt.fields
import feincms.module.mixins


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0001_initial'),
        ('biographies', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApplicationContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('parameters', feincms.contrib.fields.JSONField(null=True, editable=False)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('urlconf_path', models.CharField(max_length=100, verbose_name='application', choices=[(b'registration.urls', b'Registration application')])),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'application contents',
                'db_table': 'page_page_applicationcontent',
                'verbose_name': 'application content',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BiographyContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'biography contents',
                'db_table': 'page_page_biographycontent',
                'verbose_name': 'biography content',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CalendarContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('calendar_src', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'calendar contents',
                'db_table': 'page_page_calendarcontent',
                'verbose_name': 'calendar content',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GalleryContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('gallery', models.ForeignKey(to='galleries.Gallery')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'gallery contents',
                'db_table': 'page_page_gallerycontent',
                'verbose_name': 'gallery content',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImageContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=content.models.getUploadTo, max_length=255, verbose_name='image')),
                ('alt_text', models.CharField(help_text='Description of image', max_length=255, verbose_name='alternate text', blank=True)),
                ('caption', models.CharField(max_length=255, verbose_name='caption', blank=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('position', models.CharField(default=b'left', max_length=10, verbose_name='position', choices=[(b'left', b'Float to left'), (b'right', b'Float to right'), (b'block', b'Block')])),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'images',
                'db_table': 'page_page_imagecontent',
                'verbose_name': 'image',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('active', models.BooleanField(default=True, verbose_name='active')),
                ('title', models.CharField(help_text='This title is also used for navigation menu items.', max_length=200, verbose_name='title')),
                ('slug', models.SlugField(help_text='This is used to build the URL for this page', max_length=150, verbose_name='slug')),
                ('in_navigation', models.BooleanField(default=False, verbose_name='in navigation')),
                ('override_url', models.CharField(help_text="Override the target URL. Be sure to include slashes at the beginning and at the end if it is a local URL. This affects both the navigation and subpages' URLs.", max_length=255, verbose_name='override URL', blank=True)),
                ('redirect_to', models.CharField(help_text='Target URL for automatic redirects or the primary key of a page.', max_length=255, verbose_name='redirect to', blank=True)),
                ('_cached_url', models.CharField(default='', editable=False, max_length=255, blank=True, verbose_name='Cached URL', db_index=True)),
                ('navigation_extension', models.CharField(help_text='Select the module providing subpages for this page if you need to customize the navigation.', max_length=200, null=True, verbose_name='navigation extension', blank=True)),
                ('publication_date', models.DateTimeField(default=feincms.module.extensions.datepublisher.granular_now, verbose_name='publication date')),
                ('publication_end_date', models.DateTimeField(help_text='Leave empty if the entry should stay active forever.', null=True, verbose_name='publication end date', blank=True)),
                ('_content_title', models.TextField(help_text='The first line is the main title, the following lines are subtitles.', verbose_name='content title', blank=True)),
                ('_page_title', models.CharField(help_text='Page title for browser window. Same as title bydefault. Must not be longer than 70 characters.', max_length=69, verbose_name='page title', blank=True)),
                ('template_key', models.CharField(default=b'basic.html', max_length=255, verbose_name='template', choices=[(b'basic.html', 'Standard template')])),
                ('parent', models.ForeignKey(related_name='children', verbose_name='Parent', blank=True, to='page.Page', null=True)),
            ],
            options={
                'ordering': ['tree_id', 'lft'],
                'verbose_name': 'page',
                'verbose_name_plural': 'pages',
            },
            bases=(models.Model, feincms.extensions.ExtensionsMixin, feincms.module.mixins.ContentModelMixin),
        ),
        migrations.CreateModel(
            name='PhotoLink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'gallery_link_photos')),
                ('alt', models.CharField(max_length=200)),
                ('caption', models.CharField(max_length=30, blank=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('page', mptt.fields.TreeForeignKey(related_name='link_to', to='page.Page')),
                ('parent', models.ForeignKey(related_name='photolink_set', to='page.Page')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'photo links',
                'db_table': 'page_page_photolink',
                'verbose_name': 'photo link',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RichTextContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', feincms.contrib.richtext.RichTextField(verbose_name='text', blank=True)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(related_name='richtextcontent_set', to='page.Page')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'rich texts',
                'db_table': 'page_page_richtextcontent',
                'verbose_name': 'rich text',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubtitledHeader',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('heading', models.CharField(max_length=100)),
                ('subtitle', models.CharField(max_length=200)),
                ('region', models.CharField(max_length=255)),
                ('ordering', models.IntegerField(default=0, verbose_name='ordering')),
                ('parent', models.ForeignKey(related_name='subtitledheader_set', to='page.Page')),
            ],
            options={
                'ordering': ['ordering'],
                'abstract': False,
                'verbose_name_plural': 'subtitled headers',
                'db_table': 'page_page_subtitledheader',
                'verbose_name': 'subtitled header',
                'permissions': [],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='imagecontent',
            name='parent',
            field=models.ForeignKey(related_name='imagecontent_set', to='page.Page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gallerycontent',
            name='parent',
            field=models.ForeignKey(related_name='gallerycontent_set', to='page.Page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calendarcontent',
            name='parent',
            field=models.ForeignKey(related_name='calendarcontent_set', to='page.Page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='biographycontent',
            name='parent',
            field=models.ForeignKey(related_name='biographycontent_set', to='page.Page'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='biographycontent',
            name='section',
            field=models.ForeignKey(to='biographies.BiographySection'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='applicationcontent',
            name='parent',
            field=models.ForeignKey(related_name='applicationcontent_set', to='page.Page'),
            preserve_default=True,
        ),
    ]
