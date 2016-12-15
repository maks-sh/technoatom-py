# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-15 10:57
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0004_merge_20161214_1922'),
    ]

    operations = [
        migrations.AddField(
            model_name='chargecategory',
            name='cat_type',
            field=models.CharField(default='', max_length=2, verbose_name='Category type'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2016, 12, 15)),
        ),
    ]
