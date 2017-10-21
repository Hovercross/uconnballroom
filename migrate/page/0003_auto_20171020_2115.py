# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0002_auto_20160730_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationcontent',
            name='urlconf_path',
            field=models.CharField(choices=[('registration.urls', 'Registration application'), ('compresults.urls', 'Competition Results application')], verbose_name='application', max_length=100),
        ),
    ]
