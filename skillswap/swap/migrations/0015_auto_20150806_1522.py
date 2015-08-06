# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0014_auto_20150805_1627'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='street',
            new_name='streetaddress',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='streetnumber',
        ),
    ]
