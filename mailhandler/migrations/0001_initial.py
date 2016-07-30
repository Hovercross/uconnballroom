# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0001_initial'),
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingListMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('from_address', models.EmailField(max_length=254)),
                ('from_name', models.CharField(max_length=254)),
                ('return_path', models.EmailField(max_length=254)),
                ('subject', models.TextField()),
                ('incoming_message_id', models.CharField(max_length=254)),
                ('body_text', models.TextField()),
                ('body_html', models.TextField(blank=True)),
                ('sent', models.BooleanField(default=False)),
                ('message_id', models.CharField(max_length=254, blank=True)),
                ('people', models.ManyToManyField(to='registration.Person')),
            ],
        ),
        migrations.CreateModel(
            name='MailingListMessageAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('attachment', models.FileField(upload_to='attachments')),
                ('cid', models.CharField(max_length=254, null=True, blank=True)),
                ('message', models.ForeignKey(to='mailhandler.MailingListMessage')),
            ],
        ),
        migrations.CreateModel(
            name='MailSender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('from_address', models.EmailField(max_length=254)),
                ('rewrite_from_name', models.TextField(max_length=200, blank=True)),
                ('rewrite_from_address', models.EmailField(max_length=254, blank=True)),
                ('unrestricted_send', models.BooleanField(default=False)),
                ('send_to_lists', models.ManyToManyField(to='lists.List', blank=True)),
            ],
        ),
    ]
