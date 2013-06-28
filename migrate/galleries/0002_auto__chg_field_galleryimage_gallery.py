# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'GalleryImage.gallery'
        db.alter_column(u'galleries_galleryimage', 'gallery_id', self.gf('adminsortable.fields.SortableForeignKey')(to=orm['galleries.Gallery']))

    def backwards(self, orm):

        # Changing field 'GalleryImage.gallery'
        db.alter_column(u'galleries_galleryimage', 'gallery_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['galleries.Gallery']))

    models = {
        u'galleries.gallery': {
            'Meta': {'object_name': 'Gallery'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'galleries.galleryimage': {
            'Meta': {'ordering': "['order']", 'object_name': 'GalleryImage'},
            'caption': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'gallery': ('adminsortable.fields.SortableForeignKey', [], {'to': u"orm['galleries.Gallery']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1', 'db_index': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['galleries']