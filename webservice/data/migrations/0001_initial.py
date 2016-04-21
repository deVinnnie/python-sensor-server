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
                ('company_id', models.AutoField(db_column='Company_ID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', blank=True, max_length=45)),
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
                ('gateway_id', models.AutoField(db_column='Gateway_ID', primary_key=True, serialize=False)),
                ('active', models.BooleanField(default=True)),
                ('api_key', data.fields.UUIDField(editable=False, default=uuid.uuid4)),
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
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('attribute', models.CharField(db_column='Attribute', max_length=45)),
                ('value', models.CharField(db_column='Value', blank=True, max_length=200)),
                ('confirmed', models.BooleanField(default=False)),
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
                ('installation_id', models.AutoField(db_column='Installation_ID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', blank=True, max_length=45)),
                ('storage_on_remote', models.BooleanField(db_column='Storage_On_Remote', default=False)),
                ('remote_database_id', models.IntegerField(db_column='Remote_Database_ID', blank=True, null=True)),
                ('active', models.BooleanField(default=True)),
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
                ('measurement_id', models.AutoField(db_column='Measurement_ID', primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(db_column='Timestamp')),
                ('value', models.FloatField(db_column='Value', blank=True, null=True)),
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
                ('measurementTypeID', models.AutoField(db_column='MeasurementTypeID', primary_key=True, serialize=False)),
                ('unit', models.CharField(db_column='Unit', blank=True, max_length=45)),
                ('scalar', models.IntegerField(db_column='Scalar', blank=True, null=True)),
                ('name', models.CharField(db_column='Name', blank=True, max_length=45)),
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
                ('permission_id', models.AutoField(db_column='Permission_ID', primary_key=True, serialize=False)),
                ('entity', models.CharField(db_column='Entity', max_length=45)),
                ('identifier', models.IntegerField(db_column='Identifier')),
                ('action', models.CharField(db_column='Action', max_length=45)),
            ],
            options={
                'db_table': 'Permission',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RemoteDatabase',
            fields=[
                ('remote_database_id', models.IntegerField(db_column='Remote_Database_ID', primary_key=True, serialize=False)),
                ('url', models.CharField(db_column='URL', blank=True, max_length=300)),
                ('username', models.CharField(db_column='Username', blank=True, max_length=45)),
                ('password', models.CharField(db_column='Password', blank=True, max_length=45)),
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
                ('sensor_id', models.AutoField(db_column='Sensor_ID', primary_key=True, serialize=False)),
                ('name', models.CharField(db_column='Name', blank=True, max_length=45, default='Sensor Node')),
                ('position_long', models.FloatField(db_column='Position_Long', blank=True, null=True)),
                ('position_lat', models.FloatField(db_column='Position_Lat', blank=True, null=True)),
                ('gateway', models.ForeignKey(related_name='sensors', db_column='Gateway_ID', to='data.Gateway', default='1')),
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
                ('id', models.AutoField(db_column='id', primary_key=True, serialize=False)),
                ('attribute', models.CharField(db_column='Attribute', max_length=45)),
                ('value', models.CharField(db_column='Value', blank=True, max_length=200)),
                ('confirmed', models.BooleanField(default=False)),
                ('sensor', models.ForeignKey(related_name='config', db_column='Sensor_ID', to='data.Sensor')),
            ],
            options={
                'managed': True,
                'db_table': 'Sensor_Configuration',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('template_id', models.AutoField(db_column='Permission_ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=45)),
                ('entityType', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'Template',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TemplateParameter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.CharField(db_column='Attribute', max_length=45)),
                ('value', models.CharField(db_column='Value', blank=True, max_length=200)),
                ('template', models.ForeignKey(to='data.Template', related_name='params')),
            ],
            options={
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
            field=models.ForeignKey(to='data.Installation', null=True, db_column='Installation_ID', blank=True, related_name='gateways'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='company',
            field=models.ForeignKey(to='data.Company', related_name='alerts'),
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
            name='measurementTypeID',
            field=models.ForeignKey(related_name='alerts', db_column='MeasurementTypeID', to='data.MeasurementType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='sensor',
            field=models.ForeignKey(related_name='alerts', db_column='Sensor_ID', to='data.Sensor'),
            preserve_default=True,
        ),
    ]
