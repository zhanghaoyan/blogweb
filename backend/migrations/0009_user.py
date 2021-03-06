# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-11 14:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_article_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=64, unique=True)),
                ('passwd', models.CharField(max_length=256)),
                ('telphone', models.IntegerField(default=None)),
                ('wechat', models.CharField(default=None, max_length=128)),
                ('qq', models.IntegerField(default=None)),
                ('email', models.CharField(default=None, max_length=32)),
            ],
        ),
    ]
