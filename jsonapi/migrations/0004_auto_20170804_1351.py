# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 13:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jsonapi', '0003_auto_20170804_1335'),
    ]

    operations = [
        migrations.RenameField(
            model_name='study',
            old_name='name',
            new_name='studyName',
        ),
    ]