# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('costumes', '0003_maintenance'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenance',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
