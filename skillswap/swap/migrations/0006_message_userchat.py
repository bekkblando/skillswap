# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('swap', '0005_auto_20150727_0428'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('text', models.CharField(max_length=300)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['datetime'],
            },
        ),
        migrations.CreateModel(
            name='UserChat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('user1', models.ForeignKey(related_name='user1', to='swap.Profile')),
                ('user2', models.ForeignKey(related_name='user2', to='swap.Profile')),
            ],
        ),
    ]
