# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0003_auto_20170721_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='BackendFileStatusModel',
            fields=[
                ('filename', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('modified_date', models.DateTimeField(auto_now_add=True)),
                ('enabled_date', models.DateTimeField(auto_now_add=True)),
                ('in_use', models.BooleanField(default=False)),
            ],
        ),
    ]
