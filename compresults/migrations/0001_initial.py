# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('order', models.PositiveIntegerField(default=0, db_index=True, editable=False)),
                ('name', models.CharField(max_length=254)),
                ('note', models.CharField(max_length=254, blank=True)),
                ('numbers', models.TextField(blank=True)),
                ('show', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
                'ordering': ['order'],
            },
        ),
    ]
