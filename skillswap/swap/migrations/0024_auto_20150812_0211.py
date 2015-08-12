# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0023_auto_20150812_0208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(13), django.core.validators.MaxValueValidator(120)], null=True, blank=True),
        ),
    ]
