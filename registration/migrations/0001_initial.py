# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'registration_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, blank=True)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('peoplesoft_number', self.gf('django.db.models.fields.CharField')(max_length=10, blank=True)),
            ('netid', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('hometown', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('major', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'registration', ['Person'])

        # Adding model 'PersonEmail'
        db.create_table(u'registration_personemail', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Person'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('send', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'registration', ['PersonEmail'])

        # Adding model 'List'
        db.create_table(u'registration_list', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50)),
        ))
        db.send_create_signal(u'registration', ['List'])

        # Adding M2M table for field included_lists on 'List'
        db.create_table(u'registration_list_included_lists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_list', models.ForeignKey(orm[u'registration.list'], null=False)),
            ('to_list', models.ForeignKey(orm[u'registration.list'], null=False))
        ))
        db.create_unique(u'registration_list_included_lists', ['from_list_id', 'to_list_id'])

        # Adding M2M table for field included_people on 'List'
        db.create_table(u'registration_list_included_people', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('list', models.ForeignKey(orm[u'registration.list'], null=False)),
            ('person', models.ForeignKey(orm[u'registration.person'], null=False))
        ))
        db.create_unique(u'registration_list_included_people', ['list_id', 'person_id'])

        # Adding model 'PersonType'
        db.create_table(u'registration_persontype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('usg_person_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('csc_semester_standing', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('student_rate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('uconn_student', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'registration', ['PersonType'])

        # Adding model 'RegistrationSession'
        db.create_table(u'registration_registrationsession', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')()),
            ('semester', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('card_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=4)),
            ('base_price', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('team_surcharge', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('nonstudent_surcharge', self.gf('django.db.models.fields.DecimalField')(max_digits=5, decimal_places=2)),
            ('returning_discount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('early_discount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('early_deadline', self.gf('django.db.models.fields.DateField')(null=True)),
            ('club_paid_list', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['registration.List'])),
            ('team_paid_list', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['registration.List'])),
            ('club_unpaid_list', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['registration.List'])),
            ('team_unpaid_list', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['registration.List'])),
        ))
        db.send_create_signal(u'registration', ['RegistrationSession'])

        # Adding model 'Registration'
        db.create_table(u'registration_registration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.Person'])),
            ('registration_session', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.RegistrationSession'])),
            ('person_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.PersonType'])),
            ('registered_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('team', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('paid_amount', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2)),
            ('paid_date', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('sent_registration_email', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'registration', ['Registration'])

        # Adding model 'MembershipCard'
        db.create_table(u'registration_membershipcard', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('membership_card', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('registration', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.Registration'], unique=True)),
        ))
        db.send_create_signal(u'registration', ['MembershipCard'])

        # Adding model 'RegistrationLocator'
        db.create_table(u'registration_registrationlocator', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('registration', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.Registration'], unique=True)),
        ))
        db.send_create_signal(u'registration', ['RegistrationLocator'])

        # Adding model 'MailSender'
        db.create_table(u'registration_mailsender', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_address', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('rewrite_from_name', self.gf('django.db.models.fields.TextField')(max_length=200, blank=True)),
            ('rewrite_from_address', self.gf('django.db.models.fields.EmailField')(max_length=254, blank=True)),
            ('unrestricted_send', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'registration', ['MailSender'])

        # Adding M2M table for field send_to_lists on 'MailSender'
        db.create_table(u'registration_mailsender_send_to_lists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailsender', models.ForeignKey(orm[u'registration.mailsender'], null=False)),
            ('list', models.ForeignKey(orm[u'registration.list'], null=False))
        ))
        db.create_unique(u'registration_mailsender_send_to_lists', ['mailsender_id', 'list_id'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'registration_person')

        # Deleting model 'PersonEmail'
        db.delete_table(u'registration_personemail')

        # Deleting model 'List'
        db.delete_table(u'registration_list')

        # Removing M2M table for field included_lists on 'List'
        db.delete_table('registration_list_included_lists')

        # Removing M2M table for field included_people on 'List'
        db.delete_table('registration_list_included_people')

        # Deleting model 'PersonType'
        db.delete_table(u'registration_persontype')

        # Deleting model 'RegistrationSession'
        db.delete_table(u'registration_registrationsession')

        # Deleting model 'Registration'
        db.delete_table(u'registration_registration')

        # Deleting model 'MembershipCard'
        db.delete_table(u'registration_membershipcard')

        # Deleting model 'RegistrationLocator'
        db.delete_table(u'registration_registrationlocator')

        # Deleting model 'MailSender'
        db.delete_table(u'registration_mailsender')

        # Removing M2M table for field send_to_lists on 'MailSender'
        db.delete_table('registration_mailsender_send_to_lists')


    models = {
        u'registration.list': {
            'Meta': {'object_name': 'List'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'included_lists': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'included_lists_rel_+'", 'to': u"orm['registration.List']"}),
            'included_people': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registration.Person']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50'})
        },
        u'registration.mailsender': {
            'Meta': {'object_name': 'MailSender'},
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rewrite_from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'rewrite_from_name': ('django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'}),
            'send_to_lists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registration.List']", 'symmetrical': 'False'}),
            'unrestricted_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'registration.membershipcard': {
            'Meta': {'object_name': 'MembershipCard'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership_card': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'registration': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['registration.Registration']", 'unique': 'True'})
        },
        u'registration.person': {
            'Meta': {'object_name': 'Person'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'hometown': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'netid': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'peoplesoft_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'registration.personemail': {
            'Meta': {'object_name': 'PersonEmail'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.Person']"}),
            'send': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'registration.persontype': {
            'Meta': {'object_name': 'PersonType'},
            'csc_semester_standing': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student_rate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uconn_student': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'usg_person_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'registration.registration': {
            'Meta': {'object_name': 'Registration'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'paid_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'paid_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.Person']"}),
            'person_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.PersonType']"}),
            'registered_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'registration_session': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.RegistrationSession']"}),
            'sent_registration_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'registration.registrationlocator': {
            'Meta': {'object_name': 'RegistrationLocator'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'registration': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['registration.Registration']", 'unique': 'True'})
        },
        u'registration.registrationsession': {
            'Meta': {'object_name': 'RegistrationSession'},
            'base_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'card_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'club_paid_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['registration.List']"}),
            'club_unpaid_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['registration.List']"}),
            'early_deadline': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'early_discount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nonstudent_surcharge': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'returning_discount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'team_paid_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['registration.List']"}),
            'team_surcharge': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'team_unpaid_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['registration.List']"}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['registration']