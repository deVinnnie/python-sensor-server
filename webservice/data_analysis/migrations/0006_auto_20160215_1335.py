# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_analysis', '0005_auto_20160212_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='installation',
            name='storage_on_remote',
            field=models.BooleanField(default=1, db_column='Storage_On_Remote'),
            preserve_default=True,
        ),
    ]
