# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0003_auto_20150725_0151'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='skilllearn',
            name='rank',
        ),
    ]
