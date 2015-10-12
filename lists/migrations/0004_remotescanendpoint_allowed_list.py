# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_remotescanendpoint_remotescanuuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='remotescanendpoint',
            name='allowed_list',
            field=models.ForeignKey(blank=True, to='lists.QueryList', null=True),
        ),
    ]
