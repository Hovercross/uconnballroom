# -*- coding: utf-8 -*-


from django.db import models, migrations
import adminsortable.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Biography',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(default=1, editable=False, db_index=True)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=50, null=True, blank=True)),
                ('email', models.EmailField(max_length=75, null=True, blank=True)),
                ('biography', models.TextField(null=True, blank=True)),
                ('photo', models.ImageField(null=True, upload_to=b'bio_photos', blank=True)),
            ],
            options={
                'ordering': ['order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BiographySection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=50)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='biography',
            name='section',
            field=adminsortable.fields.SortableForeignKey(to='biographies.BiographySection'),
            preserve_default=True,
        ),
    ]
