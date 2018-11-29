# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccd', '0003_auto_20181119_1448'),
    ]

    operations = [
        migrations.RenameField(
            model_name='state',
            old_name='state',
            new_name='description',
        ),
        migrations.RemoveField(
            model_name='student',
            name='id',
        ),
        migrations.AlterField(
            model_name='student',
            name='rollNo',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]
