# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-24 11:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0009_auto_20170730_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='paymenttransaction',
            name='voucher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='payments.Voucher', verbose_name='voucher'),
        ),
    ]
