# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('membership_card', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=200, blank=True)),
                ('last_name', models.CharField(max_length=200, blank=True)),
                ('gender', models.CharField(blank=True, max_length=1, choices=[(b'M', b'Male'), (b'F', b'Female')])),
                ('phone_number', models.CharField(max_length=20, blank=True)),
                ('peoplesoft_number', models.CharField(max_length=10, blank=True)),
                ('netid', models.CharField(max_length=8, blank=True)),
                ('hometown', models.CharField(max_length=100, blank=True)),
                ('major', models.CharField(max_length=200, blank=True)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=254)),
                ('send', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('person', models.ForeignKey(related_name='emails', to='registration.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, editable=False, db_index=True)),
                ('description', models.CharField(max_length=50)),
                ('usg_person_type', models.CharField(max_length=50)),
                ('csc_semester_standing', models.CharField(max_length=50, blank=True)),
                ('student_rate', models.BooleanField()),
                ('uconn_student', models.BooleanField()),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PersonTypeAutoList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('list_name', models.CharField(max_length=50)),
                ('person_type', models.ForeignKey(to='registration.PersonType')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('registered_at', models.DateTimeField(auto_now_add=True)),
                ('team', models.BooleanField()),
                ('paid_amount', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('paid_date', models.DateTimeField(null=True, blank=True)),
                ('sent_registration_email', models.BooleanField(default=False)),
                ('notes', models.TextField(blank=True)),
                ('person', models.ForeignKey(to='registration.Person')),
                ('person_type', models.ForeignKey(to='registration.PersonType')),
            ],
            options={
                'permissions': (('can_run_reports', 'Can run reports'), ('can_manage_payments', 'Can manage payments'), ('can_autocomplete', 'Can use autocomplete'), ('entry_tracker', 'Can use entry tracker')),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RegistrationSession',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('year', models.IntegerField()),
                ('semester', models.CharField(max_length=10)),
                ('card_code', models.CharField(unique=True, max_length=4)),
                ('base_price', models.DecimalField(max_digits=5, decimal_places=2)),
                ('team_surcharge', models.DecimalField(default=0, max_digits=5, decimal_places=2, blank=True)),
                ('nonstudent_surcharge', models.DecimalField(default=0, max_digits=5, decimal_places=2, blank=True)),
                ('returning_discount', models.DecimalField(default=0, max_digits=5, decimal_places=2, blank=True)),
                ('early_discount', models.DecimalField(default=0, max_digits=5, decimal_places=2, blank=True)),
                ('early_deadline', models.DateField(null=True, blank=True)),
                ('first_club_day', models.DateField(null=True, blank=True)),
                ('last_free_day', models.DateField(null=True, blank=True)),
                ('available', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='registration',
            name='registration_session',
            field=models.ForeignKey(to='registration.RegistrationSession'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='registration',
            unique_together=set([('person', 'registration_session')]),
        ),
        migrations.AddField(
            model_name='membershipcard',
            name='registration',
            field=models.OneToOneField(to='registration.Registration'),
            preserve_default=True,
        ),
    ]
