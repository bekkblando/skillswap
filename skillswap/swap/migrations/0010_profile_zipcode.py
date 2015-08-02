# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0009_profile_recommendation'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='zipcode',
            field=models.CharField(max_length=5, default=29609),
            preserve_default=False,
        ),
    ]
