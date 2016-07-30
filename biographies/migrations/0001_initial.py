# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Biography',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, default=0, editable=False)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50, blank=True, null=True)),
                ('email', models.EmailField(max_length=254, blank=True, null=True)),
                ('biography', models.TextField(blank=True, null=True)),
                ('photo', models.ImageField(upload_to='bio_photos', blank=True, null=True)),
            ],
            options={
                'abstract': False,
                'ordering': ['order'],
            },
        ),
        migrations.CreateModel(
            name='BiographySection',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='biography',
            name='section',
            field=adminsortable.fields.SortableForeignKey(to='biographies.BiographySection'),
        ),
    ]
