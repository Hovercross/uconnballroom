# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'List.internally_managed'
        db.add_column(u'registration_list', 'internally_managed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'List.internally_managed'
        db.delete_column(u'registration_list', 'internally_managed')


    models = {
        u'registration.list': {
            'Meta': {'object_name': 'List'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'included_lists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registration.List']", 'symmetrical': 'False', 'blank': 'True'}),
            'included_people': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registration.Person']", 'symmetrical': 'False', 'blank': 'True'}),
            'internally_managed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'emails'", 'to': u"orm['registration.Person']"}),
            'send': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'registration.persontype': {
            'Meta': {'ordering': "['order']", 'object_name': 'PersonType'},
            'csc_semester_standing': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'student_rate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'uconn_student': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'usg_person_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'registration.persontypeautolist': {
            'Meta': {'object_name': 'PersonTypeAutoList'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'person_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['registration.PersonType']"})
        },
        u'registration.registration': {
            'Meta': {'unique_together': "(('person', 'registration_session'),)", 'object_name': 'Registration'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'paid_amount': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'paid_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'base_price': ('django.db.models.fields.DecimalField', [], {'max_digits': '5', 'decimal_places': '2'}),
            'card_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'club_paid_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['registration.List']"}),
            'club_unpaid_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['registration.List']"}),
            'early_deadline': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'early_discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'first_club_day': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_free_day': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'nonstudent_surcharge': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'returning_discount': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'semester': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'team_paid_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['registration.List']"}),
            'team_surcharge': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'team_unpaid_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['registration.List']"}),
            'year': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['registration']