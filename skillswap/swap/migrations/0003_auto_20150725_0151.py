# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('swap', '0002_delete_skill'),
    ]

    operations = [
        migrations.CreateModel(
            name='Meeting',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('meeting', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=140)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('phone', models.CharField(max_length=18, blank=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')])),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=140)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SkillKnow',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('rank', models.IntegerField()),
                ('description', models.TextField()),
                ('skill', models.ForeignKey(to='swap.Skill')),
                ('user', models.ForeignKey(to='swap.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='SkillLearn',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('rank', models.IntegerField()),
                ('description', models.TextField()),
                ('skill', models.ForeignKey(to='swap.Skill')),
                ('user', models.ForeignKey(to='swap.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='learn',
            field=models.ManyToManyField(to='swap.Skill', related_name='learn', through='swap.SkillLearn'),
        ),
        migrations.AddField(
            model_name='profile',
            name='skills',
            field=models.ManyToManyField(to='swap.Skill', related_name='skills', through='swap.SkillKnow'),
        ),
        migrations.AddField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='meeting',
            name='usercommentedon',
            field=models.ForeignKey(related_name='commentedon', to='swap.Profile'),
        ),
        migrations.AddField(
            model_name='meeting',
            name='usercommenting',
            field=models.ForeignKey(related_name='commenter', to='swap.Profile'),
        ),
    ]
