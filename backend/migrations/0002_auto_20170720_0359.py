# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-20 03:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FrontendFileStatus',
            new_name='FrontendFileStatusModel',
        ),
    ]