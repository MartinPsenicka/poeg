# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-19 16:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import poeg.apps.games.models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0002_auto_20170516_1626'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActiveGameLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts_start', models.DateTimeField(auto_now_add=True)),
                ('ts_finish', models.DateTimeField(blank=True, null=True)),
                ('active_game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.ActiveGame', verbose_name='active game')),
                ('quest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Quest', verbose_name='active quest')),
            ],
        ),
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ('homepageorder',)},
        ),
        migrations.AlterModelOptions(
            name='hint',
            options={'ordering': ('order',)},
        ),
        migrations.AlterField(
            model_name='hint',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=poeg.apps.games.models.hint_image_upload_to, verbose_name='image'),
        ),
        migrations.AddField(
            model_name='activegamelog',
            name='used_hints',
            field=models.ManyToManyField(blank=True, to='games.Hint'),
        ),
        migrations.AlterUniqueTogether(
            name='activegamelog',
            unique_together=set([('active_game', 'quest')]),
        ),
    ]
