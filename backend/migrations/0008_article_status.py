# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-07 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20170407_1130'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
