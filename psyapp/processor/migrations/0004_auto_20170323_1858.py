# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-23 13:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('processor', '0003_auto_20170323_1847'),
    ]

    operations = [
        migrations.AlterField(
            model_name='strategy',
            name='ticker',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='processor.Ticker'),
        ),
        migrations.AlterField(
            model_name='ticker',
            name='exchange',
            field=models.CharField(choices=[('nse', 'nse')], default='nse', max_length=6),
        ),
    ]
