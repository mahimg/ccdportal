# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='states',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('state', models.CharField(max_length=200)),
                ('updatedOn', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='student',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('rollNo', models.CharField(max_length=20)),
                ('currentState', models.CharField(max_length=200)),
                ('lastUpdated', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='states',
            name='student',
            field=models.ForeignKey(to='ccd.student'),
        ),
        migrations.AddField(
            model_name='states',
            name='updatedBy',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
