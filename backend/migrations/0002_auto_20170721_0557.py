# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-21 05:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='frontendfilestatusmodel',
            name='enabled_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]