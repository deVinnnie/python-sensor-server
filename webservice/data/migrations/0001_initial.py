# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import data.fields
import uuid


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
                ('name', models.CharField(max_length=45, blank=True, db_column='Name')),
                ('active', models.BooleanField(default=True)),
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
                ('gateway_id', models.AutoField(primary_key=True, serialize=False, db_column='Gateway_ID')),
                ('active', models.BooleanField(default=True)),
                ('api_key', data.fields.UUIDField(default=uuid.uuid4, editable=False)),
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
                ('id', models.AutoField(primary_key=True, serialize=False, db_column='id')),
                ('attribute', models.CharField(max_length=45, db_column='Attribute')),
                ('value', models.CharField(max_length=200, blank=True, db_column='Value')),
                ('confirmed', models.BooleanField(default=False)),
                ('gateway', models.ForeignKey(to='data.Gateway', db_column='Gateway_ID', related_name='config')),
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
                ('installation_id', models.AutoField(primary_key=True, serialize=False, db_column='Installation_ID')),
                ('name', models.CharField(max_length=45, blank=True, db_column='Name')),
                ('storage_on_remote', models.BooleanField(default=False, db_column='Storage_On_Remote')),
                ('remote_database_id', models.IntegerField(blank=True, null=True, db_column='Remote_Database_ID')),
                ('active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(to='data.Company', db_column='Company_ID', related_name='installations')),
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
                ('measurement_id', models.AutoField(primary_key=True, serialize=False, db_column='Measurement_ID')),
                ('timestamp', models.DateTimeField(db_column='Timestamp')),
                ('value', models.FloatField(blank=True, null=True, db_column='Value')),
                ('alert', models.BooleanField(default=False)),
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
                ('measurementTypeID', models.AutoField(primary_key=True, serialize=False, db_column='MeasurementTypeID')),
                ('unit', models.CharField(max_length=45, blank=True, db_column='Unit')),
                ('scalar', models.IntegerField(blank=True, null=True, db_column='Scalar')),
                ('name', models.CharField(max_length=45, blank=True, db_column='Name')),
                ('upper_bound', models.IntegerField(default=27)),
                ('lower_bound', models.IntegerField(default=0)),
            ],
            options={
                'managed': True,
                'db_table': 'MeasurementType',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('permission_id', models.AutoField(primary_key=True, serialize=False, db_column='Permission_ID')),
                ('entity', models.CharField(max_length=45, db_column='Entity')),
                ('identifier', models.IntegerField(db_column='Identifier')),
                ('action', models.CharField(max_length=45, db_column='Action')),
            ],
            options={
                'db_table': 'Permission',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RemoteDatabase',
            fields=[
                ('remote_database_id', models.IntegerField(primary_key=True, serialize=False, db_column='Remote_Database_ID')),
                ('url', models.CharField(max_length=300, blank=True, db_column='URL')),
                ('username', models.CharField(max_length=45, blank=True, db_column='Username')),
                ('password', models.CharField(max_length=45, blank=True, db_column='Password')),
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
                ('sensor_id', models.AutoField(primary_key=True, serialize=False, db_column='Sensor_ID')),
                ('name', models.CharField(default='Sensor Node', max_length=45, blank=True, db_column='Name')),
                ('position_long', models.FloatField(blank=True, null=True, db_column='Position_Long')),
                ('position_lat', models.FloatField(blank=True, null=True, db_column='Position_Lat')),
                ('gateway', models.ForeignKey(to='data.Gateway', db_column='Gateway_ID', related_name='sensors', default='1')),
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
                ('id', models.AutoField(primary_key=True, serialize=False, db_column='id')),
                ('attribute', models.CharField(max_length=45, db_column='Attribute')),
                ('value', models.CharField(max_length=200, blank=True, db_column='Value')),
                ('confirmed', models.BooleanField(default=False)),
                ('sensor', models.ForeignKey(to='data.Sensor', db_column='Sensor_ID', related_name='config')),
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
            field=models.ForeignKey(to='data.MeasurementType', db_column='Measurement_Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurement',
            name='sensor',
            field=models.ForeignKey(to='data.Sensor', db_column='Sensor_ID', related_name='measurements'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='gatewayconfiguration',
            unique_together=set([('gateway', 'attribute')]),
        ),
        migrations.AddField(
            model_name='gateway',
            name='installation',
            field=models.ForeignKey(to='data.Installation', blank=True, db_column='Installation_ID', related_name='gateways', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='company',
            field=models.ForeignKey(related_name='alerts', to='data.Company'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='gateway',
            field=models.ForeignKey(to='data.Gateway', db_column='Gateway_ID', related_name='alerts'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='measurementTypeID',
            field=models.ForeignKey(to='data.MeasurementType', db_column='MeasurementTypeID', related_name='alerts'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='sensor',
            field=models.ForeignKey(to='data.Sensor', db_column='Sensor_ID', related_name='alerts'),
            preserve_default=True,
        ),
    ]
