# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compresults', '0002_event_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='status',
            field=models.CharField(default='upcoming', choices=[('done', 'Done'), ('upcoming', 'Upcoming'), ('hidden', 'Hidden')], max_length=8),
        ),
    ]
