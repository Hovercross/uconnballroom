# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
        ('registration', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingListMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
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
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailingListMessageAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('attachment', models.FileField(upload_to=b'attachments')),
                ('cid', models.CharField(max_length=254, null=True, blank=True)),
                ('message', models.ForeignKey(to='mailhandler.MailingListMessage')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailSender',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_address', models.EmailField(max_length=254)),
                ('rewrite_from_name', models.TextField(max_length=200, blank=True)),
                ('rewrite_from_address', models.EmailField(max_length=254, blank=True)),
                ('unrestricted_send', models.BooleanField(default=False)),
                ('send_to_lists', models.ManyToManyField(to='lists.List', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
