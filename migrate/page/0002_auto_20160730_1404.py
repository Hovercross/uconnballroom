# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gallerycontent',
            name='gallery',
        ),
        migrations.RemoveField(
            model_name='gallerycontent',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='photolink',
            name='page',
        ),
        migrations.RemoveField(
            model_name='photolink',
            name='parent',
        ),
        migrations.DeleteModel(
            name='GalleryContent',
        ),
        migrations.DeleteModel(
            name='PhotoLink',
        ),
    ]
