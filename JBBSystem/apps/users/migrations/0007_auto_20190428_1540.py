# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-04-28 15:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_userprofile_is_vip'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='is_VIP',
            new_name='is_vip',
        ),
    ]
