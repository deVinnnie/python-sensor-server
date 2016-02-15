# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_analysis', '0003_auto_20160212_1311'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorconfiguration',
            name='sensor',
            field=models.ForeignKey(primary_key=True, to='data_analysis.Sensor', db_column='Sensor_ID', serialize=False),
            preserve_default=True,
        ),
    ]
