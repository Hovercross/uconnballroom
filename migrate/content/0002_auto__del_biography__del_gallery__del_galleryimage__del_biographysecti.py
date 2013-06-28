# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Biography'
        db.delete_table(u'content_biography')

        # Deleting model 'Gallery'
        db.delete_table(u'content_gallery')

        # Deleting model 'GalleryImage'
        db.delete_table(u'content_galleryimage')

        # Deleting model 'BiographySection'
        db.delete_table(u'content_biographysection')


    def backwards(self, orm):
        # Adding model 'Biography'
        db.create_table(u'content_biography', (
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('photo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('section', self.gf('adminsortable.fields.SortableForeignKey')(to=orm['content.BiographySection'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True, blank=True)),
            ('biography', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'content', ['Biography'])

        # Adding model 'Gallery'
        db.create_table(u'content_gallery', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'content', ['Gallery'])

        # Adding model 'GalleryImage'
        db.create_table(u'content_galleryimage', (
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('gallery', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['content.Gallery'])),
            ('caption', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=1, db_index=True)),
        ))
        db.send_create_signal(u'content', ['GalleryImage'])

        # Adding model 'BiographySection'
        db.create_table(u'content_biographysection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal(u'content', ['BiographySection'])


    models = {
        
    }

    complete_apps = ['content']