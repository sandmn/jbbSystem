# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-17 14:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_video_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='学习时长（分钟数）'),
        ),
    ]