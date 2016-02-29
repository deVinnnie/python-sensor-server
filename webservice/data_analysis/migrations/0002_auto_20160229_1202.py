# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_analysis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SensorConfiguration',
            fields=[
                ('attribute', models.CharField(max_length=45, primary_key=True, serialize=False)),
                ('value', models.CharField(db_column='Value', blank=True, max_length=200)),
                ('sensor', models.ForeignKey(to='data_analysis.Sensor', db_column='Sensor_ID', related_name='config')),
            ],
            options={
                'db_table': 'Sensor_Configuration',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='sensor',
            name='gateway',
        ),
        migrations.AddField(
            model_name='sensor',
            name='gateway_id',
            field=models.ForeignKey(to='data_analysis.Gateway', db_column='Gateway_ID', default='1', related_name='sensors'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gateway',
            name='gateway_id',
            field=models.IntegerField(db_column='Gateway_ID', primary_key=True, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gateway',
            name='installation',
            field=models.ForeignKey(to='data_analysis.Installation', db_column='Installation_ID', null=True, blank=True, related_name='gateways'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gatewayconfiguration',
            name='attribute',
            field=models.CharField(db_column='Attribute', max_length=45, primary_key=True, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gatewayconfiguration',
            name='gateway',
            field=models.ForeignKey(to='data_analysis.Gateway', db_column='Gateway_ID', related_name='config'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='installation',
            name='company',
            field=models.ForeignKey(to='data_analysis.Company', db_column='Company_ID', related_name='installations'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='installation',
            name='installation_id',
            field=models.IntegerField(db_column='Installation_ID', primary_key=True, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='installation',
            name='storage_on_remote',
            field=models.IntegerField(db_column='Storage_On_Remote'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='measurement',
            name='sensor_id',
            field=models.ForeignKey(to='data_analysis.Sensor', db_column='Sensor_ID', related_name='measurements'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='measurementtype',
            name='measurementTypeID',
            field=models.IntegerField(db_column='MeasurementTypeID', primary_key=True, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='remotedatabase',
            name='remote_database_id',
            field=models.IntegerField(db_column='Remote_Database_ID', primary_key=True, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensor_id',
            field=models.IntegerField(db_column='Sensor_ID', primary_key=True, serialize=False),
            preserve_default=True,
        ),
    ]
