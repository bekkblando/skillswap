# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0021_auto_20150810_2109'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(default=18, validators=[django.core.validators.MinValueValidator(13), django.core.validators.MaxValueValidator(120)]),
            preserve_default=False,
        ),
    ]
