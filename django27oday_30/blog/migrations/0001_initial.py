# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Playvideo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('videoname', models.FileField(upload_to=b'./static/angularjsfile/video/')),
                ('img', models.FileField(upload_to=b'./static/angularjsfile/img/')),
                ('playnum', models.CharField(max_length=30)),
                ('intvideo', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=80)),
                ('checkcode', models.CharField(max_length=30)),
            ],
        ),
    ]
