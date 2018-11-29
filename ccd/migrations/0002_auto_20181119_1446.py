# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccd', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='currentState',
            new_name='lastState',
        ),
        migrations.AlterField(
            model_name='states',
            name='student',
            field=models.ForeignKey(to='ccd.Student'),
        ),
    ]
