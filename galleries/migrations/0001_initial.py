# -*- coding: utf-8 -*-


from django.db import models, migrations
import galleries.models
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, editable=False, db_index=True)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GalleryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, editable=False, db_index=True)),
                ('image', models.ImageField(upload_to=galleries.models.getGalleryImagePath)),
                ('title', models.CharField(max_length=50, null=True, blank=True)),
                ('caption', models.TextField(null=True, blank=True)),
                ('gallery', adminsortable.fields.SortableForeignKey(to='galleries.Gallery')),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
