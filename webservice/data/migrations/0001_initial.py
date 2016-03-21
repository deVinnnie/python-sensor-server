# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('text', models.CharField(max_length=500)),
                ('url', models.URLField()),
                ('archived', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.AutoField(primary_key=True, serialize=False, db_column='Company_ID')),
                ('name', models.CharField(max_length=45, db_column='Name', blank=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'Company',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Gateway',
            fields=[
                ('gateway_id', models.AutoField(primary_key=True, serialize=False, db_column='Gateway_ID')),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'db_table': 'Gateway',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GatewayConfiguration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, db_column='id')),
                ('attribute', models.CharField(max_length=45, db_column='Attribute')),
                ('value', models.CharField(max_length=200, db_column='Value', blank=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('gateway', models.ForeignKey(related_name='config', db_column='Gateway_ID', to='data.Gateway')),
            ],
            options={
                'db_table': 'Gateway_Configuration',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Installation',
            fields=[
                ('installation_id', models.AutoField(primary_key=True, serialize=False, db_column='Installation_ID')),
                ('name', models.CharField(max_length=45, db_column='Name', blank=True)),
                ('storage_on_remote', models.BooleanField(db_column='Storage_On_Remote', default=False)),
                ('remote_database_id', models.IntegerField(db_column='Remote_Database_ID', blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(related_name='installations', db_column='Company_ID', to='data.Company')),
            ],
            options={
                'db_table': 'Installation',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('measurement_id', models.AutoField(primary_key=True, serialize=False, db_column='Measurement_ID')),
                ('timestamp', models.DateTimeField(db_column='Timestamp')),
                ('value', models.FloatField(db_column='Value', blank=True, null=True)),
            ],
            options={
                'db_table': 'Measurement',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MeasurementType',
            fields=[
                ('measurementTypeID', models.IntegerField(primary_key=True, serialize=False, db_column='MeasurementTypeID')),
                ('unit', models.CharField(max_length=45, db_column='Unit', blank=True)),
                ('scalar', models.IntegerField(db_column='Scalar', blank=True, null=True)),
                ('name', models.CharField(max_length=45, db_column='Name', blank=True)),
            ],
            options={
                'db_table': 'MeasurementType',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RemoteDatabase',
            fields=[
                ('remote_database_id', models.IntegerField(primary_key=True, serialize=False, db_column='Remote_Database_ID')),
                ('url', models.CharField(max_length=300, db_column='URL', blank=True)),
                ('username', models.CharField(max_length=45, db_column='Username', blank=True)),
                ('password', models.CharField(max_length=45, db_column='Password', blank=True)),
            ],
            options={
                'db_table': 'Remote_Database',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('sensor_id', models.AutoField(primary_key=True, serialize=False, db_column='Sensor_ID')),
                ('name', models.CharField(max_length=45, db_column='Name', blank=True, default='Sensor Node')),
                ('position_long', models.DecimalField(max_digits=10, db_column='Position_Long', decimal_places=0, blank=True, null=True)),
                ('position_lat', models.DecimalField(max_digits=10, db_column='Position_Lat', decimal_places=0, blank=True, null=True)),
                ('gateway', models.ForeignKey(related_name='sensors', db_column='Gateway_ID', default='1', to='data.Gateway')),
            ],
            options={
                'db_table': 'Sensor',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SensorConfiguration',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, db_column='id')),
                ('attribute', models.CharField(max_length=45, db_column='Attribute')),
                ('value', models.CharField(max_length=200, db_column='Value', blank=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('sensor', models.ForeignKey(related_name='config', db_column='Sensor_ID', to='data.Sensor')),
            ],
            options={
                'db_table': 'Sensor_Configuration',
                'managed': True,
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
            field=models.ForeignKey(related_name='gateways', db_column='Installation_ID', null=True, blank=True, to='data.Installation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='company',
            field=models.ForeignKey(related_name='alerts', to='data.Company'),
            preserve_default=True,
        ),
    ]
