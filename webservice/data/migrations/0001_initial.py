# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuid
import data.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
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
                ('company_id', models.AutoField(db_column='Company_ID', serialize=False, primary_key=True)),
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
                ('gateway_id', models.AutoField(db_column='Gateway_ID', serialize=False, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('api_key', data.fields.UUIDField(editable=False, default=uuid.uuid4)),
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
                ('id', models.AutoField(db_column='id', serialize=False, primary_key=True)),
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
                ('installation_id', models.AutoField(db_column='Installation_ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=45, db_column='Name', blank=True)),
                ('storage_on_remote', models.BooleanField(db_column='Storage_On_Remote', default=False)),
                ('remote_database_id', models.IntegerField(null=True, db_column='Remote_Database_ID', blank=True)),
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
                ('measurement_id', models.AutoField(db_column='Measurement_ID', serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(db_column='Timestamp')),
                ('value', models.FloatField(null=True, db_column='Value', blank=True)),
                ('alert', models.BooleanField(default=False)),
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
                ('measurementTypeID', models.AutoField(db_column='MeasurementTypeID', serialize=False, primary_key=True)),
                ('unit', models.CharField(max_length=45, db_column='Unit', blank=True)),
                ('scalar', models.IntegerField(null=True, db_column='Scalar', blank=True)),
                ('name', models.CharField(max_length=45, db_column='Name', blank=True)),
                ('upper_bound', models.IntegerField(default=27)),
                ('lower_bound', models.IntegerField(default=0)),
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
                ('remote_database_id', models.IntegerField(db_column='Remote_Database_ID', serialize=False, primary_key=True)),
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
                ('sensor_id', models.AutoField(db_column='Sensor_ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=45, db_column='Name', default='Sensor Node', blank=True)),
                ('position_long', models.FloatField(null=True, db_column='Position_Long', blank=True)),
                ('position_lat', models.FloatField(null=True, db_column='Position_Lat', blank=True)),
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
                ('id', models.AutoField(db_column='id', serialize=False, primary_key=True)),
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
            field=models.ForeignKey(blank=True, null=True, db_column='Installation_ID', related_name='gateways', to='data.Installation'),
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
            field=models.ForeignKey(related_name='alerts', db_column='Gateway_ID', to='data.Gateway'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='sensor',
            field=models.ForeignKey(related_name='alerts', db_column='Sensor_ID', to='data.Sensor'),
            preserve_default=True,
        ),
    ]
