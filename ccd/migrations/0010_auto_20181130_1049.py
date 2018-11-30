# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccd', '0009_auto_20181130_1049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='state',
            name='student',
            field=models.ForeignKey(to='ccd.Student'),
        ),
    ]
