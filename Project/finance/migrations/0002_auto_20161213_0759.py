# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-13 07:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('finance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='username',
            field=models.CharField(max_length=255, verbose_name='phone'),
        ),
    ]
