# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'MailingListMessage.to_address'
        db.delete_column('mailhandler_mailinglistmessage', 'to_address')

        # Adding M2M table for field people on 'MailingListMessage'
        m2m_table_name = db.shorten_name('mailhandler_mailinglistmessage_people')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('mailinglistmessage', models.ForeignKey(orm['mailhandler.mailinglistmessage'], null=False)),
            ('person', models.ForeignKey(orm['registration.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['mailinglistmessage_id', 'person_id'])


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'MailingListMessage.to_address'
        raise RuntimeError("Cannot reverse this migration. 'MailingListMessage.to_address' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'MailingListMessage.to_address'
        db.add_column('mailhandler_mailinglistmessage', 'to_address',
                      self.gf('django.db.models.fields.EmailField')(max_length=254),
                      keep_default=False)

        # Removing M2M table for field people on 'MailingListMessage'
        db.delete_table(db.shorten_name('mailhandler_mailinglistmessage_people'))


    models = {
        'mailhandler.mailinglistmessage': {
            'Meta': {'object_name': 'MailingListMessage'},
            'body_html': ('django.db.models.fields.TextField', [], {}),
            'body_text': ('django.db.models.fields.TextField', [], {}),
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'from_name': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incoming_message_id': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'people': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['registration.Person']", 'symmetrical': 'False'}),
            'return_path': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject': ('django.db.models.fields.TextField', [], {})
        },
        'mailhandler.mailinglistmessageattachment': {
            'Meta': {'object_name': 'MailingListMessageAttachment'},
            'attachment': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'cid': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['mailhandler.MailingListMessage']"})
        },
        'mailhandler.mailsender': {
            'Meta': {'object_name': 'MailSender'},
            'from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rewrite_from_address': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'rewrite_from_name': ('django.db.models.fields.TextField', [], {'max_length': '200', 'blank': 'True'}),
            'send_to_lists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['registration.List']", 'symmetrical': 'False', 'blank': 'True'}),
            'unrestricted_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'registration.list': {
            'Meta': {'object_name': 'List'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'included_lists': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['registration.List']", 'symmetrical': 'False', 'blank': 'True'}),
            'included_people': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['registration.Person']", 'symmetrical': 'False', 'blank': 'True'}),
            'list_type': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'unrestricted_send': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
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
        }
    }

    complete_apps = ['mailhandler']