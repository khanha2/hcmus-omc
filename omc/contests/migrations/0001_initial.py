# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-04 03:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('name', models.CharField(max_length=200)),
                ('from_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('to_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('short_description', models.TextField(blank=True, default=None, null=True)),
                ('description', models.TextField(blank=True, default=None, null=True)),
                ('contest_time', models.PositiveIntegerField(default=0)),
                ('maximum_of_matches', models.PositiveIntegerField(default=0)),
                ('use_mc_test', models.BooleanField(default=False)),
                ('mc_test_questions', models.PositiveIntegerField(default=0)),
                ('use_writing_test', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('participated', models.BooleanField(default=False)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.Contest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContestManager',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.Contest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_deleted', models.BooleanField(default=False)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted_date', models.DateTimeField(blank=True, default=None, null=True)),
                ('match_id', models.PositiveSmallIntegerField()),
                ('writing_test_questions', models.TextField(blank=True, default='[]', null=True)),
                ('writing_test_responses', models.TextField(blank=True, default='{}', null=True)),
                ('mc_test_questions', models.TextField(blank=True, default='[]', null=True)),
                ('mc_test_responses', models.TextField(blank=True, default='{}', null=True)),
                ('mc_test_passed_responses', models.PositiveIntegerField(default=0)),
                ('start_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('end_time', models.DateTimeField(blank=True, default=None, null=True)),
                ('contestant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.Contestant')),
            ],
        ),
        migrations.CreateModel(
            name='MCQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='')),
                ('a', models.TextField(default=None, null=True)),
                ('b', models.TextField(default=None, null=True)),
                ('c', models.TextField(default=None, null=True)),
                ('d', models.TextField(default=None, null=True)),
                ('answer', models.CharField(default=None, max_length=2, null=True)),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.Contest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='WritingQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='')),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contests.Contest')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterUniqueTogether(
            name='match',
            unique_together=set([('contestant', 'match_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='contestmanager',
            unique_together=set([('contest', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='contestant',
            unique_together=set([('contest', 'user')]),
        ),
    ]
