# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MailingListMessage'
        db.create_table(u'mailhandler_mailinglistmessage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('from_address', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('from_name', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('return_path', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('to_address', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('subject', self.gf('django.db.models.fields.TextField')()),
            ('incoming_message_id', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('body_text', self.gf('django.db.models.fields.TextField')()),
            ('body_html', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'mailhandler', ['MailingListMessage'])

        # Adding model 'Attachment'
        db.create_table(u'mailhandler_attachment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['mailhandler.MailingListMessage'])),
            ('attachment', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('mime_type', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'mailhandler', ['Attachment'])


    def backwards(self, orm):
        # Deleting model 'MailingListMessage'
        db.delete_table(u'mailhandler_mailinglistmessage')

        # Deleting model 'Attachment'
        db.delete_table(u'mailhandler_attachment')


    models = {
        u'mailhandler.attachment': {
            'Meta': {'object_name': 'Attachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mailhandler.MailingListMessage']"}),
            'mime_type': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'mailhandler.mailinglistmessage': {
            'Meta': {'object_name': 'MailingListMessage'},
            'body_html': ('django.db.models.fields.TextField', [], {}),
            'body_text': ('django.db.models.fields.TextField', [], {}),
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incoming_message_id': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'return_path': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'subject': ('django.db.models.fields.TextField', [], {}),
            'to_address': ('django.db.models.fields.EmailField', [], {'max_length': '254'})
        },
        u'mailhandler.mailsender': {
            'Meta': {'object_name': 'MailSender'},
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rewrite_from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'rewrite_from_name': ('django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'}),
            'send_to_lists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registration.List']", 'symmetrical': 'False', 'blank': 'True'}),
            'unrestricted_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'registration.list': {
            'Meta': {'object_name': 'List'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'included_lists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registration.List']", 'symmetrical': 'False', 'blank': 'True'}),
            'included_people': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registration.Person']", 'symmetrical': 'False', 'blank': 'True'}),
            'list_type': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
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