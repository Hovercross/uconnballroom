# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import galleries.models
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(editable=False, db_index=True, default=0)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(editable=False, db_index=True, default=0)),
                ('image', models.ImageField(upload_to=galleries.models.getGalleryImagePath)),
                ('title', models.CharField(max_length=50, null=True, blank=True)),
                ('caption', models.TextField(null=True, blank=True)),
                ('gallery', adminsortable.fields.SortableForeignKey(to='galleries.Gallery')),
            ],
            options={
                'abstract': False,
                'ordering': ['order'],
            },
        ),
    ]
