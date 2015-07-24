# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('swap', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('meeting', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('address', models.CharField(max_length=140)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('phone', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SkillData',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('rank', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='skill',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='skilldata',
            name='skill',
            field=models.ForeignKey(to='swap.Skill'),
        ),
        migrations.AddField(
            model_name='skilldata',
            name='user',
            field=models.ForeignKey(to='swap.Profile'),
        ),
        migrations.AddField(
            model_name='profile',
            name='learn',
            field=models.ManyToManyField(related_name='learn', to='swap.Skill'),
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(related_name='skills', to='swap.Skill', through='swap.SkillData'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='meeting',
            name='usercommentedon',
            field=models.ForeignKey(to='swap.Profile', related_name='commentedon'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='usercommenting',
            field=models.ForeignKey(to='swap.Profile', related_name='commenter'),
        ),
    ]
