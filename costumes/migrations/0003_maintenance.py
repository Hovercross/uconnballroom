# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
        ('costumes', '0002_auto_20170708_2324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('maintenance_date', models.DateField()),
                ('did_clean', models.BooleanField()),
                ('did_rhinestone', models.BooleanField()),
                ('did_sew', models.BooleanField()),
                ('costume', models.ForeignKey(to='costumes.Costume')),
                ('fixer', models.ForeignKey(to='registration.Person')),
            ],
        ),
    ]
