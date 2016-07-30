# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('list_type', models.CharField(max_length=254, choices=[('entry_list', 'Entry List'), ('person_type_list', 'Person Type List'), ('registration_type_list', 'Club/Team List'), ('paid_list', 'Paid Tracking List'), ('admin_list', 'Administrative List')])),
                ('people', models.ManyToManyField(to='registration.Person', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='QueryList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.SlugField(unique=True)),
                ('unrestricted_send', models.BooleanField(default=False)),
                ('query_string', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='RemoteScanEndpoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=255)),
                ('title', models.CharField(max_length=50)),
                ('auth_key', models.CharField(max_length=40, unique=True)),
                ('list_prefix', models.CharField(max_length=255, blank=True)),
                ('allowed_list', models.ForeignKey(to='lists.QueryList', null=True, blank=True)),
                ('scan_list', models.ForeignKey(to='lists.List', null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='RemoteScanUUID',
            fields=[
                ('uuid', models.UUIDField(serialize=False, primary_key=True, editable=False)),
            ],
        ),
    ]
