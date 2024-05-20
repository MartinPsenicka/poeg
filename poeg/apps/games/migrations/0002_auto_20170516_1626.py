# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-16 14:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_activated', models.DateTimeField(auto_now_add=True, verbose_name='activated')),
                ('ts_finished', models.DateTimeField(blank=True, null=True, verbose_name='finished')),
                ('activation_type', models.CharField(blank=True, choices=[('gratis_martin', 'gratis Martin'), ('gratis_lucka', 'gratis Lucka'), ('voucher_own', 'voucher own'), ('voucher_slevomat', 'voucher Slevomat')], max_length=50, verbose_name='activation type')),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='games.Game', verbose_name='gameid')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='activegame',
            unique_together=set([('game', 'user', 'ts_finished')]),
        ),
    ]