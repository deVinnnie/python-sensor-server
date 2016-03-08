# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.AutoField(primary_key=True, db_column='Company_ID', serialize=False)),
                ('name', models.CharField(blank=True, max_length=45, db_column='Name')),
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
                ('ip_address', models.CharField(blank=True, max_length=45, db_column='IP-address')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('attribute', models.CharField(max_length=45, db_column='Attribute')),
                ('value', models.CharField(blank=True, max_length=200, db_column='Value')),
                ('gateway', models.ForeignKey(related_name='config', db_column='Gateway_ID', to='data_analysis.Gateway')),
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
                ('storage_on_remote', models.IntegerField(db_column='Storage_On_Remote', blank=True, default=0)),
                ('remote_database_id', models.IntegerField(null=True, blank=True, db_column='Remote_Database_ID')),
                ('company', models.ForeignKey(related_name='installations', db_column='Company_ID', to='data_analysis.Company')),
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
                ('value', models.DecimalField(max_digits=10, null=True, decimal_places=5, blank=True, db_column='Value')),
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
                ('scalar', models.IntegerField(null=True, blank=True, db_column='Scalar')),
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
                ('name', models.CharField(db_column='Name', blank=True, max_length=45, default='Sensor Node')),
                ('position_long', models.DecimalField(max_digits=10, null=True, decimal_places=0, blank=True, db_column='Position_Long')),
                ('position_lat', models.DecimalField(max_digits=10, null=True, decimal_places=0, blank=True, db_column='Position_Lat')),
                ('gateway_id', models.ForeignKey(related_name='sensors', db_column='Gateway_ID', default='1', to='data_analysis.Gateway')),
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
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('attribute', models.CharField(max_length=45, db_column='Attribute')),
                ('value', models.CharField(blank=True, max_length=200, db_column='Value')),
                ('sensor', models.ForeignKey(related_name='config', db_column='Sensor_ID', to='data_analysis.Sensor')),
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
            field=models.ForeignKey(to='data_analysis.MeasurementType', db_column='Measurement_Type'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurement',
            name='sensor_id',
            field=models.ForeignKey(related_name='measurements', db_column='Sensor_ID', to='data_analysis.Sensor'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='gatewayconfiguration',
            unique_together=set([('gateway', 'attribute')]),
        ),
        migrations.AddField(
            model_name='gateway',
            name='installation',
            field=models.ForeignKey(to='data_analysis.Installation', db_column='Installation_ID', related_name='gateways', null=True, blank=True),
            preserve_default=True,
        ),
    ]
