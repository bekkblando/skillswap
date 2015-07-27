# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0004_remove_skilllearn_rank'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='address',
            new_name='city',
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.CharField(default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='street',
            field=models.CharField(default=1, max_length=140),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='streetnumber',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
