# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-31 18:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0010_paymenttransaction_voucher'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='multiple_use',
            field=models.BooleanField(default=False, verbose_name='multiple usage'),
        ),
    ]