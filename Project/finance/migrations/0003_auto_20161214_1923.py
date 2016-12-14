# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-14 16:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0002_auto_20161213_2045'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='activation_key',
            field=models.CharField(blank=True, max_length=40),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='key_expires',
            field=models.DateTimeField(default=datetime.date(2016, 12, 14)),
        ),
        migrations.AlterModelTable(
            name='chargecategory',
            table='finance_chargecategory',
        ),
    ]
