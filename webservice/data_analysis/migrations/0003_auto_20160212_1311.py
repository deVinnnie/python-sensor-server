# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_analysis', '0002_auto_20160212_1306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gatewayconfiguration',
            name='gateway',
            field=models.ForeignKey(primary_key=True, to='data_analysis.Gateway', db_column='Gateway_ID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='measurement',
            name='measurement_type',
            field=models.ForeignKey(to='data_analysis.MeasurementType', db_column='Measurement_Type'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='measurement',
            name='sensor_id',
            field=models.ForeignKey(to='data_analysis.Sensor', db_column='Sensor_ID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensorconfiguration',
            name='sensor',
            field=models.ForeignKey(primary_key=True, to='data_analysis.Sensor', db_column='Sensor_ID'),
            preserve_default=True,
        ),
    ]
