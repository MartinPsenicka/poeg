# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-01 14:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0005_quest_after_quest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activegame',
            name='activation_type',
            field=models.CharField(blank=True, choices=[('gratis_martin', 'gratis Martin'), ('gratis_lucka', 'gratis Lucka'), ('voucher_own', 'voucher own'), ('voucher_slevomat', 'voucher Slevomat'), ('bankwire', 'platba převodem')], max_length=50, verbose_name='activation type'),
        ),
    ]
