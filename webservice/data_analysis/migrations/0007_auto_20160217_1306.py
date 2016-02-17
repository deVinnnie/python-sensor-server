# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_analysis', '0006_auto_20160215_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='company_id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='Company_ID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gateway',
            name='gateway_id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='Gateway_ID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='installation',
            name='installation_id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='Installation_ID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='measurement',
            name='measurement_id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='Measurement_ID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='measurementtype',
            name='measurementTypeID',
            field=models.AutoField(serialize=False, primary_key=True, db_column='MeasurementTypeID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='remotedatabase',
            name='remote_database_id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='Remote_Database_ID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensor_id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='Sensor_ID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensorconfiguration',
            name='sensor',
            field=models.ForeignKey(to='data_analysis.Sensor', primary_key=True, db_column='Sensor_ID'),
            preserve_default=True,
        ),
    ]
