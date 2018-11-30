# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccd', '0006_update'),
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('name', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AlterField(
            model_name='state',
            name='student',
            field=models.ForeignKey(to='ccd.Student'),
        ),
    ]
