# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0010_profile_zipcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='city',
            field=models.CharField(max_length=140, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='state',
            field=models.CharField(max_length=2, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='street',
            field=models.CharField(max_length=140, blank=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='zipcode',
            field=models.CharField(max_length=5, blank=True),
        ),
    ]
