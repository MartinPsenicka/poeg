# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-23 16:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20170516_1454'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='newsletter',
            field=models.BooleanField(default=True, verbose_name='informovat o novinkách'),
        ),
        migrations.AlterField(
            model_name='user',
            name='teamname',
            field=models.CharField(blank=True, help_text='Jméno Vašeho týmu', max_length=50, null=True, unique=True, verbose_name='teamname'),
        ),
    ]