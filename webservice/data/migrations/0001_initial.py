# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import data.fields


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
                ('company_id', models.AutoField(primary_key=True, db_column='Company_ID', serialize=False)),
                ('name', models.CharField(blank=True, max_length=45, db_column='Name')),
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
                ('gateway_id', models.AutoField(primary_key=True, db_column='Gateway_ID', serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('api_key', data.fields.UUIDField()),
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
                ('id', models.AutoField(primary_key=True, db_column='id', serialize=False)),
                ('attribute', models.CharField(max_length=45, db_column='Attribute')),
                ('value', models.CharField(blank=True, max_length=200, db_column='Value')),
                ('confirmed', models.BooleanField(default=False)),
                ('gateway', models.ForeignKey(db_column='Gateway_ID', related_name='config', to='data.Gateway')),
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
                ('installation_id', models.AutoField(primary_key=True, db_column='Installation_ID', serialize=False)),
                ('name', models.CharField(blank=True, max_length=45, db_column='Name')),
                ('storage_on_remote', models.IntegerField(blank=True, db_column='Storage_On_Remote', default=0)),
                ('remote_database_id', models.IntegerField(blank=True, db_column='Remote_Database_ID', null=True)),
                ('active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(db_column='Company_ID', related_name='installations', to='data.Company')),
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
                ('measurement_id', models.AutoField(primary_key=True, db_column='Measurement_ID', serialize=False)),
                ('timestamp', models.DateTimeField(db_column='Timestamp')),
                ('value', models.FloatField(blank=True, db_column='Value', null=True)),
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
                ('measurementTypeID', models.IntegerField(primary_key=True, db_column='MeasurementTypeID', serialize=False)),
                ('unit', models.CharField(blank=True, max_length=45, db_column='Unit')),
                ('scalar', models.IntegerField(blank=True, db_column='Scalar', null=True)),
                ('name', models.CharField(blank=True, max_length=45, db_column='Name')),
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
                ('remote_database_id', models.IntegerField(primary_key=True, db_column='Remote_Database_ID', serialize=False)),
                ('url', models.CharField(blank=True, max_length=300, db_column='URL')),
                ('username', models.CharField(blank=True, max_length=45, db_column='Username')),
                ('password', models.CharField(blank=True, max_length=45, db_column='Password')),
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
                ('sensor_id', models.AutoField(primary_key=True, db_column='Sensor_ID', serialize=False)),
                ('name', models.CharField(blank=True, max_length=45, db_column='Name', default='Sensor Node')),
                ('position_long', models.DecimalField(blank=True, db_column='Position_Long', max_digits=10, null=True, decimal_places=0)),
                ('position_lat', models.DecimalField(blank=True, db_column='Position_Lat', max_digits=10, null=True, decimal_places=0)),
                ('gateway', models.ForeignKey(db_column='Gateway_ID', related_name='sensors', to='data.Gateway', default='1')),
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
                ('id', models.AutoField(primary_key=True, db_column='id', serialize=False)),
                ('attribute', models.CharField(max_length=45, db_column='Attribute')),
                ('value', models.CharField(blank=True, max_length=200, db_column='Value')),
                ('confirmed', models.BooleanField(default=False)),
                ('sensor', models.ForeignKey(db_column='Sensor_ID', related_name='config', to='data.Sensor')),
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
            field=models.ForeignKey(db_column='Sensor_ID', related_name='measurements', to='data.Sensor'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='gatewayconfiguration',
            unique_together=set([('gateway', 'attribute')]),
        ),
        migrations.AddField(
            model_name='gateway',
            name='installation',
            field=models.ForeignKey(db_column='Installation_ID', null=True, blank=True, related_name='gateways', to='data.Installation'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='company',
            field=models.ForeignKey(related_name='alerts', to='data.Company'),
            preserve_default=True,
        ),
    ]
