# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-16 12:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170515_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='lang',
            field=models.CharField(blank=True, choices=[('cs', 'Czech')], help_text='Language ISO.', max_length=5, verbose_name='prefered lang'),
        ),
    ]
