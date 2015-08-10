# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0018_auto_20150808_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='Age',
            field=models.IntegerField(default=18, validators=[django.core.validators.MinValueValidator(13), django.core.validators.MaxValueValidator(120)]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(max_length=7, blank=True, choices=[('Female', 'Female'), ('Male', 'Male')]),
        ),
    ]
