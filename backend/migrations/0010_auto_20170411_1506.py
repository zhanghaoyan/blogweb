# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-11 15:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='qq',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='telphone',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='uid',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='wechat',
            field=models.CharField(max_length=128, null=True),
        ),
    ]
