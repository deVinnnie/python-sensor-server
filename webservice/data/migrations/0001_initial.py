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
                ('name', models.CharField(db_column='Name', blank=True, max_length=45)),
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
                ('attribute', models.CharField(db_column='Attribute', max_length=45)),
                ('value', models.CharField(db_column='Value', blank=True, max_length=200)),
                ('confirmed', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('gateway', models.ForeignKey(db_column='Gateway_ID', to='data.Gateway', related_name='config')),
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
                ('name', models.CharField(db_column='Name', blank=True, max_length=45)),
                ('storage_on_remote', models.BooleanField(default=False, db_column='Storage_On_Remote')),
                ('remote_database_id', models.IntegerField(null=True, db_column='Remote_Database_ID', blank=True)),
                ('active', models.BooleanField(default=True)),
                ('company', models.ForeignKey(db_column='Company_ID', to='data.Company', related_name='installations')),
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
                ('unit', models.CharField(db_column='Unit', blank=True, max_length=45)),
                ('scalar', models.IntegerField(null=True, db_column='Scalar', blank=True)),
                ('name', models.CharField(db_column='Name', blank=True, max_length=45)),
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
                ('url', models.CharField(db_column='URL', blank=True, max_length=300)),
                ('username', models.CharField(db_column='Username', blank=True, max_length=45)),
                ('password', models.CharField(db_column='Password', blank=True, max_length=45)),
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
                ('name', models.CharField(default='Sensor Node', db_column='Name', blank=True, max_length=45)),
                ('position_long', models.DecimalField(null=True, db_column='Position_Long', blank=True, decimal_places=0, max_digits=10)),
                ('position_lat', models.DecimalField(null=True, db_column='Position_Lat', blank=True, decimal_places=0, max_digits=10)),
                ('gateway', models.ForeignKey(db_column='Gateway_ID', related_name='sensors', default='1', to='data.Gateway')),
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
                ('attribute', models.CharField(db_column='Attribute', max_length=45)),
                ('value', models.CharField(db_column='Value', blank=True, max_length=200)),
                ('confirmed', models.BooleanField(default=False)),
                ('deleted', models.BooleanField(default=False)),
                ('sensor', models.ForeignKey(db_column='Sensor_ID', to='data.Sensor', related_name='config')),
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
            field=models.ForeignKey(to='data.MeasurementType', db_column='Measurement_Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurement',
            name='sensor_id',
            field=models.ForeignKey(db_column='Sensor_ID', to='data.Sensor', related_name='measurements'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='gatewayconfiguration',
            unique_together=set([('gateway', 'attribute')]),
        ),
        migrations.AddField(
            model_name='gateway',
            name='installation',
            field=models.ForeignKey(db_column='Installation_ID', blank=True, related_name='gateways', to='data.Installation', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='alert',
            name='company',
            field=models.ForeignKey(to='data.Company', related_name='alerts'),
            preserve_default=True,
        ),
    ]
