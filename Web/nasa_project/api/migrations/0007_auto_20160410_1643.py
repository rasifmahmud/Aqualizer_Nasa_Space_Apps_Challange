# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-10 16:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20160410_1641'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='waterparticle',
            name='id',
        ),
        migrations.AlterField(
            model_name='waterparticle',
            name='deviceID',
            field=models.CharField(default=1, max_length=50, primary_key=True, serialize=False),
            preserve_default=False,
        ),
    ]
