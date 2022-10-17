# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-31 11:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20190428_1608'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='estimate',
            field=models.CharField(choices=[('best', '优'), ('good', '良'), ('normal', '中'), ('bad', '差')], default='', max_length=10),
        ),
    ]