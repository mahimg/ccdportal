# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ccd', '0002_auto_20181119_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('state', models.CharField(max_length=200)),
                ('updatedOn', models.DateTimeField(auto_now_add=True)),
                ('student', models.ForeignKey(to='ccd.Student')),
                ('updatedBy', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='states',
            name='student',
        ),
        migrations.RemoveField(
            model_name='states',
            name='updatedBy',
        ),
        migrations.DeleteModel(
            name='states',
        ),
    ]
