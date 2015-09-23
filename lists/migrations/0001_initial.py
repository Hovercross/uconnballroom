# -*- coding: utf-8 -*-


from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='List',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('list_type', models.CharField(max_length=254, choices=[(b'entry_list', b'Entry List'), (b'person_type_list', b'Person Type List'), (b'registration_type_list', b'Club/Team List'), (b'paid_list', b'Paid Tracking List'), (b'admin_list', b'Administrative List')])),
                ('people', models.ManyToManyField(to='registration.Person', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='QueryList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('slug', models.SlugField(unique=True)),
                ('unrestricted_send', models.BooleanField(default=False)),
                ('query_string', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
