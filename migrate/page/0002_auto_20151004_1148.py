# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationcontent',
            name='urlconf_path',
            field=models.CharField(verbose_name='application', choices=[('registration.urls', 'Registration application')], max_length=100),
        ),
        migrations.AlterField(
            model_name='imagecontent',
            name='position',
            field=models.CharField(verbose_name='position', max_length=10, choices=[('left', 'Float to left'), ('right', 'Float to right'), ('block', 'Block')], default='left'),
        ),
        migrations.AlterField(
            model_name='page',
            name='_page_title',
            field=models.CharField(help_text='Page title for browser window. Same as title by default. Must be 69 characters or fewer.', verbose_name='page title', max_length=69, blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='template_key',
            field=models.CharField(verbose_name='template', max_length=255, choices=[('basic.html', 'Standard template')], default='basic.html'),
        ),
        migrations.AlterField(
            model_name='photolink',
            name='image',
            field=models.ImageField(upload_to='gallery_link_photos'),
        ),
    ]
