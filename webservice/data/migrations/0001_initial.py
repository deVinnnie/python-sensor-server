# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import data.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.AutoField(serialize=False, primary_key=True, db_column='Company_ID')),
                ('name', models.CharField(max_length=45, db_column='Name', blank=True)),
            ],
            options={
                'managed': True,
                'db_table': 'Company',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('gateway_id', models.AutoField(serialize=False, primary_key=True, db_column='Gateway_ID')),
                ('api_key', data.fields.UUIDField()),
            ],
            options={
                'managed': True,
                'db_table': 'Gateway',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GatewayConfiguration',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='id')),
                ('attribute', models.CharField(max_length=45, db_column='Attribute')),
                ('value', models.CharField(max_length=200, db_column='Value', blank=True)),
                ('gateway', models.ForeignKey(related_name='config', db_column='Gateway_ID', to='data.Gateway')),
            ],
            options={
                'managed': True,
                'db_table': 'Gateway_Configuration',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('installation_id', models.AutoField(serialize=False, primary_key=True, db_column='Installation_ID')),
                ('name', models.CharField(max_length=45, db_column='Name', blank=True)),
                ('storage_on_remote', models.IntegerField(default=0, db_column='Storage_On_Remote', blank=True)),
                ('remote_database_id', models.IntegerField(db_column='Remote_Database_ID', null=True, blank=True)),
                ('company', models.ForeignKey(related_name='installations', db_column='Company_ID', to='data.Company')),
            ],
            options={
                'managed': True,
                'db_table': 'Installation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('measurement_id', models.AutoField(serialize=False, primary_key=True, db_column='Measurement_ID')),
                ('timestamp', models.DateTimeField(db_column='Timestamp')),
                ('value', models.FloatField(db_column='Value', null=True, blank=True)),
            ],
            options={
                'managed': True,
                'db_table': 'Measurement',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeasurementType',
            fields=[
                ('measurementTypeID', models.IntegerField(serialize=False, primary_key=True, db_column='MeasurementTypeID')),
                ('unit', models.CharField(max_length=45, db_column='Unit', blank=True)),
                ('scalar', models.IntegerField(db_column='Scalar', null=True, blank=True)),
                ('name', models.CharField(max_length=45, db_column='Name', blank=True)),
            ],
            options={
                'managed': True,
                'db_table': 'MeasurementType',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RemoteDatabase',
            fields=[
                ('remote_database_id', models.IntegerField(serialize=False, primary_key=True, db_column='Remote_Database_ID')),
                ('url', models.CharField(max_length=300, db_column='URL', blank=True)),
                ('username', models.CharField(max_length=45, db_column='Username', blank=True)),
                ('password', models.CharField(max_length=45, db_column='Password', blank=True)),
            ],
            options={
                'managed': True,
                'db_table': 'Remote_Database',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sensor_id', models.AutoField(serialize=False, primary_key=True, db_column='Sensor_ID')),
                ('name', models.CharField(max_length=45, default='Sensor Node', db_column='Name', blank=True)),
                ('position_long', models.DecimalField(decimal_places=0, max_digits=10, db_column='Position_Long', null=True, blank=True)),
                ('position_lat', models.DecimalField(decimal_places=0, max_digits=10, db_column='Position_Lat', null=True, blank=True)),
                ('gateway', models.ForeignKey(default='1', related_name='sensors', db_column='Gateway_ID', to='data.Gateway')),
            ],
            options={
                'managed': True,
                'db_table': 'Sensor',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SensorConfiguration',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, db_column='id')),
                ('attribute', models.CharField(max_length=45, db_column='Attribute')),
                ('value', models.CharField(max_length=200, db_column='Value', blank=True)),
                ('sensor', models.ForeignKey(related_name='config', db_column='Sensor_ID', to='data.Sensor')),
            ],
            options={
                'managed': True,
                'db_table': 'Sensor_Configuration',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='sensorconfiguration',
            unique_together=set([('sensor', 'attribute')]),
        ),
        migrations.AddField(
            model_name='measurement',
            name='measurement_type',
            field=models.ForeignKey(db_column='Measurement_Type', to='data.MeasurementType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurement',
            name='sensor_id',
            field=models.ForeignKey(related_name='measurements', db_column='Sensor_ID', to='data.Sensor'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='gatewayconfiguration',
            unique_together=set([('gateway', 'attribute')]),
        ),
        migrations.AddField(
            model_name='gateway',
            name='installation',
            field=models.ForeignKey(related_name='gateways', db_column='Installation_ID', null=True, to='data.Installation', blank=True),
            preserve_default=True,
        ),
    ]
