# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('author', models.CharField(max_length=255, null=True)),
                ('city', models.CharField(max_length=10, null=True)),
                ('category', models.CharField(max_length=2, null=True)),
                ('event', models.CharField(max_length=255, null=True)),
                ('venue', models.CharField(max_length=255, null=True)),
                ('showtime', models.DateTimeField(null=True, verbose_name=b'Event Time')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('fb_link', models.URLField(null=True)),
                ('mobile', models.CharField(max_length=20, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
