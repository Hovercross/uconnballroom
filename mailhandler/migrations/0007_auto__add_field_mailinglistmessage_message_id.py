# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MailingListMessage.message_id'
        db.add_column(u'mailhandler_mailinglistmessage', 'message_id',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=254, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MailingListMessage.message_id'
        db.delete_column(u'mailhandler_mailinglistmessage', 'message_id')


    models = {
        u'lists.list': {
            'Meta': {'object_name': 'List'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_type': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registration.Person']", 'symmetrical': 'False', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'mailhandler.mailinglistmessage': {
            'Meta': {'object_name': 'MailingListMessage'},
            'body_html': ('django.db.models.fields.TextField', [], {}),
            'body_text': ('django.db.models.fields.TextField', [], {}),
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incoming_message_id': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'message_id': ('django.db.models.fields.CharField', [], {'max_length': '254', 'blank': 'True'}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['registration.Person']", 'symmetrical': 'False'}),
            'return_path': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.TextField', [], {})
        },
        u'mailhandler.mailinglistmessageattachment': {
            'Meta': {'object_name': 'MailingListMessageAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['mailhandler.MailingListMessage']"})
        },
        u'mailhandler.mailsender': {
            'Meta': {'object_name': 'MailSender'},
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rewrite_from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'rewrite_from_name': ('django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'}),
            'send_to_lists': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['lists.List']", 'symmetrical': 'False', 'blank': 'True'}),
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