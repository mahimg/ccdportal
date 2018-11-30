# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccd', '0008_rememberpreference'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='company',
            field=models.ForeignKey(default='Accenture', to='ccd.Company'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='state',
            name='student',
            field=models.ForeignKey(to='ccd.Student'),
        ),
    ]
