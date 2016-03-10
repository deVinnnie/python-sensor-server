# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0002_auto_20160309_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gatewayconfiguration',
            name='id',
            field=models.AutoField(serialize=False, db_column='id', primary_key=True),
            preserve_default=True,
        ),
    ]
