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
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('text', models.CharField(max_length=500)),
                ('archived', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.AutoField(serialize=False, db_column='Company_ID', primary_key=True)),
                ('name', models.CharField(db_column='Name', max_length=45, blank=True)),
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
                ('gateway_id', models.AutoField(serialize=False, db_column='Gateway_ID', primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('api_key', data.fields.UUIDField(default=uuid.uuid4, editable=False)),
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
                ('id', models.AutoField(serialize=False, db_column='id', primary_key=True)),
                ('attribute', models.CharField(db_column='Attribute', max_length=45)),
                ('value', models.CharField(db_column='Value', max_length=200, blank=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('gateway', models.ForeignKey(to='data.Gateway', db_column='Gateway_ID', related_name='config')),
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
                ('installation_id', models.AutoField(serialize=False, db_column='Installation_ID', primary_key=True)),
                ('name', models.CharField(db_column='Name', max_length=45, blank=True)),
                ('storage_on_remote', models.BooleanField(db_column='Storage_On_Remote', default=False)),
                ('remote_database_id', models.IntegerField(null=True, db_column='Remote_Database_ID', blank=True)),
                ('active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(to='data.Company', db_column='Company_ID', related_name='installations')),
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
                ('measurement_id', models.AutoField(serialize=False, db_column='Measurement_ID', primary_key=True)),
                ('timestamp', models.DateTimeField(db_column='Timestamp')),
                ('value', models.FloatField(null=True, db_column='Value', blank=True)),
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
                ('measurementTypeID', models.AutoField(serialize=False, db_column='MeasurementTypeID', primary_key=True)),
                ('unit', models.CharField(db_column='Unit', max_length=45, blank=True)),
                ('scalar', models.IntegerField(null=True, db_column='Scalar', blank=True)),
                ('name', models.CharField(db_column='Name', max_length=45, blank=True)),
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
            name='Permission',
            fields=[
                ('permission_id', models.AutoField(serialize=False, db_column='Permission_ID', primary_key=True)),
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
            name='Sensor',
            fields=[
                ('sensor_id', models.AutoField(serialize=False, db_column='Sensor_ID', primary_key=True)),
                ('tag', models.CharField(db_column='Name', max_length=45, default='Sensor Node', blank=True)),
                ('position_long', models.FloatField(null=True, db_column='Position_Long', blank=True)),
                ('position_lat', models.FloatField(null=True, db_column='Position_Lat', blank=True)),
                ('last_check', models.DateTimeField(null=True, db_column='Last_Check', blank=True)),
                ('gateway', models.ForeignKey(default='1', to='data.Gateway', db_column='Gateway_ID', related_name='sensors')),
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
                ('id', models.AutoField(serialize=False, db_column='id', primary_key=True)),
                ('attribute', models.CharField(db_column='Attribute', max_length=45)),
                ('value', models.CharField(db_column='Value', max_length=200, blank=True)),
                ('confirmed', models.BooleanField(default=False)),
                ('sensor', models.ForeignKey(to='data.Sensor', db_column='Sensor_ID', related_name='config')),
            ],
            options={
                'db_table': 'Sensor_Configuration',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('template_id', models.AutoField(serialize=False, db_column='Permission_ID', primary_key=True)),
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
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('attribute', models.CharField(db_column='Attribute', max_length=45)),
                ('value', models.CharField(db_column='Value', max_length=200, blank=True)),
                ('template', models.ForeignKey(related_name='params', to='data.Template')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VagueMeasurement',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('timestamp', models.DateTimeField(db_column='Timestamp')),
                ('value', models.FloatField(null=True, db_column='Value', blank=True)),
                ('measurement_type', models.ForeignKey(db_column='Measurement_Type', to='data.MeasurementType')),
                ('sensor_id', models.ForeignKey(to='data.Sensor', db_column='Sensor_ID', related_name='overview_measurements')),
            ],
            options={
                'db_table': 'VagueMeasurement',
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
            field=models.ForeignKey(to='data.Installation', null=True, db_column='Installation_ID', related_name='gateways', blank=True),
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
            name='measurement',
            field=models.ForeignKey(to='data.Measurement', db_column='Measurement_ID', related_name='alert'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='sensor',
            field=models.ForeignKey(to='data.Sensor', db_column='Sensor_ID', related_name='alerts'),
            preserve_default=True,
        ),
    ]
