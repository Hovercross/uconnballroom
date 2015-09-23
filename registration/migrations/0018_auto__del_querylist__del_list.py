# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'QueryList'
        db.delete_table('registration_querylist')

        # Deleting model 'List'
        db.delete_table('registration_list')

        # Removing M2M table for field included_lists on 'List'
        db.delete_table(db.shorten_name('registration_list_included_lists'))

        # Removing M2M table for field included_people on 'List'
        db.delete_table(db.shorten_name('registration_list_included_people'))


    def backwards(self, orm):
        # Adding model 'QueryList'
        db.create_table('registration_querylist', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('unrestricted_send', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('query_string', self.gf('django.db.models.fields.TextField')()),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
        ))
        db.send_create_signal('registration', ['QueryList'])

        # Adding model 'List'
        db.create_table('registration_list', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('list_type', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('unrestricted_send', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('registration', ['List'])

        # Adding M2M table for field included_lists on 'List'
        m2m_table_name = db.shorten_name('registration_list_included_lists')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_list', models.ForeignKey(orm['registration.list'], null=False)),
            ('to_list', models.ForeignKey(orm['registration.list'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_list_id', 'to_list_id'])

        # Adding M2M table for field included_people on 'List'
        m2m_table_name = db.shorten_name('registration_list_included_people')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('list', models.ForeignKey(orm['registration.list'], null=False)),
            ('person', models.ForeignKey(orm['registration.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['list_id', 'person_id'])


    models = {
        'registration.membershipcard': {
            'Meta': {'object_name': 'MembershipCard'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'membership_card': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'registration': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.Registration']", 'unique': 'True'})
        },
        'registration.person': {
            'Meta': {'object_name': 'Person'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'blank': 'True'}),
            'hometown': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'major': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'netid': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'peoplesoft_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'blank': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        'registration.personemail': {
            'Meta': {'object_name': 'PersonEmail'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails'", 'to': "orm['registration.Person']"}),
            'send': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'registration.persontype': {
            'Meta': {'ordering': "['order']", 'object_name': 'PersonType'},
            'csc_semester_standing': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'student_rate': ('django.db.models.fields.BooleanField', [], {}),
            'uconn_student': ('django.db.models.fields.BooleanField', [], {}),
            'usg_person_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'registration.persontypeautolist': {
            'Meta': {'object_name': 'PersonTypeAutoList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'person_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.PersonType']"})
        },
        'registration.registration': {
            'Meta': {'unique_together': "(('person', 'registration_session'),)", 'object_name': 'Registration'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'paid_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'paid_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.Person']"}),
            'person_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.PersonType']"}),
            'registered_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'registration_session': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.RegistrationSession']"}),
            'sent_registration_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'team': ('django.db.models.fields.BooleanField', [], {})
        },
        'registration.registrationsession': {
            'Meta': {'object_name': 'RegistrationSession'},
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'base_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'card_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'early_deadline': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'early_discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'first_club_day': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_free_day': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nonstudent_surcharge': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'returning_discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'team_surcharge': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['registration']