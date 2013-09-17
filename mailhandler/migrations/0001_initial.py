# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MailSender'
        db.create_table(u'mailhandler_mailsender', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_address', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('rewrite_from_name', self.gf('django.db.models.fields.TextField')(max_length=200, blank=True)),
            ('rewrite_from_address', self.gf('django.db.models.fields.EmailField')(max_length=254, blank=True)),
            ('unrestricted_send', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'mailhandler', ['MailSender'])

        # Adding M2M table for field send_to_lists on 'MailSender'
        db.create_table(u'mailhandler_mailsender_send_to_lists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailsender', models.ForeignKey(orm[u'mailhandler.mailsender'], null=False)),
            ('list', models.ForeignKey(orm[u'registration.list'], null=False))
        ))
        db.create_unique(u'mailhandler_mailsender_send_to_lists', ['mailsender_id', 'list_id'])


    def backwards(self, orm):
        # Deleting model 'MailSender'
        db.delete_table(u'mailhandler_mailsender')

        # Removing M2M table for field send_to_lists on 'MailSender'
        db.delete_table('mailhandler_mailsender_send_to_lists')


    models = {
        u'mailhandler.mailsender': {
            'Meta': {'object_name': 'MailSender'},
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rewrite_from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'rewrite_from_name': ('django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'}),
            'send_to_lists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registration.List']", 'symmetrical': 'False'}),
            'unrestricted_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'registration.list': {
            'Meta': {'object_name': 'List'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'included_lists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registration.List']", 'symmetrical': 'False', 'blank': 'True'}),
            'included_people': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registration.Person']", 'symmetrical': 'False', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'unrestricted_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        }
    }

    complete_apps = ['mailhandler']