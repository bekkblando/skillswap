# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0008_message_sender'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='recommendation',
            field=models.ManyToManyField(related_name='recommend', to='swap.Skill'),
        ),
    ]
