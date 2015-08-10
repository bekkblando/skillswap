# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0019_auto_20150810_2059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='Age',
            new_name='age',
        ),
    ]
