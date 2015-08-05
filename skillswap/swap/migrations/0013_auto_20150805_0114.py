# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0012_auto_20150804_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='skillknow',
            name='rank',
            field=models.CharField(max_length=15),
        ),
    ]
