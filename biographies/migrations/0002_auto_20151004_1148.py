# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('biographies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='biography',
            name='email',
            field=models.EmailField(null=True, max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='biography',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='biography',
            name='photo',
            field=models.ImageField(null=True, upload_to='bio_photos', blank=True),
        ),
    ]
