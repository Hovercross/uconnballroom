# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='list',
            name='list_type',
            field=models.CharField(choices=[('entry_list', 'Entry List'), ('person_type_list', 'Person Type List'), ('registration_type_list', 'Club/Team List'), ('paid_list', 'Paid Tracking List'), ('admin_list', 'Administrative List')], max_length=254),
        ),
    ]
