# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-27 20:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20170615_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_dealer',
            field=models.BooleanField(default=False, verbose_name='voucher dealer'),
        ),
    ]
