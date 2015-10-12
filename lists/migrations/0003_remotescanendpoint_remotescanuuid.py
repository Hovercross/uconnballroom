# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0002_auto_20151004_1148'),
    ]

    operations = [
        migrations.CreateModel(
            name='RemoteScanEndpoint',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('description', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=50)),
                ('auth_key', models.CharField(unique=True, max_length=40)),
                ('list_prefix', models.CharField(blank=True, max_length=255)),
                ('scan_list', models.ForeignKey(null=True, to='lists.List', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RemoteScanUUID',
            fields=[
                ('uuid', models.UUIDField(serialize=False, primary_key=True, editable=False)),
            ],
        ),
    ]
