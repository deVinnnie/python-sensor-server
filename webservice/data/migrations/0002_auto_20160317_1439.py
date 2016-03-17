# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gateway',
            name='api_key',
        ),
        migrations.AlterField(
            model_name='installation',
            name='storage_on_remote',
            field=models.BooleanField(default=False, db_column='Storage_On_Remote'),
            preserve_default=True,
        ),
    ]
