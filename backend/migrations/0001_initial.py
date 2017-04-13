# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-04-01 06:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('aid', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('time', models.TimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Cattegory',
            fields=[
                ('cid', models.IntegerField(auto_created=True, primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Cattegory'),
        ),
    ]
