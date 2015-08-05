# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0013_auto_20150805_0114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='streetnumber',
            field=models.PositiveIntegerField(null=True, validators=[django.core.validators.MinValueValidator(1)]),
        ),
    ]
