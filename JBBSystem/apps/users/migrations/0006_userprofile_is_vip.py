# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-28 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20190419_1513'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='is_VIP',
            field=models.BooleanField(default='False', max_length=10, verbose_name='是否会员'),
        ),
    ]
