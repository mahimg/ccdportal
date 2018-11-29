# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ccd', '0004_auto_20181119_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='comments',
            field=models.CharField(max_length=200, default=''),
            preserve_default=False,
        ),
    ]
