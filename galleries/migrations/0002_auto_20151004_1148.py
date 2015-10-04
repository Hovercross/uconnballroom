# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('galleries', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='order',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
        ),
    ]
