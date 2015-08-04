# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0011_auto_20150804_2101'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='streetnumber',
            field=models.IntegerField(null=True),
        ),
    ]
