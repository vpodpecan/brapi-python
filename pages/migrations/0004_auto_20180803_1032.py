# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-08-03 10:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20180803_1025'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='html_page',
            options={'verbose_name': 'HTML page', 'verbose_name_plural': 'HTML pages'},
        ),
    ]
