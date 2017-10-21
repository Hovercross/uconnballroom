# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compresults', '0003_event_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='done',
        ),
        migrations.RemoveField(
            model_name='event',
            name='show',
        ),
    ]
