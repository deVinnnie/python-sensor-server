# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('permission_id', models.AutoField(primary_key=True, db_column='Permission_ID', serialize=False)),
                ('entity', models.CharField(max_length=45, db_column='Entity')),
                ('identifier', models.CharField(max_length=45, db_column='Identifier')),
                ('action', models.CharField(max_length=45, db_column='Action')),
            ],
            options={
                'db_table': 'Permission',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.AutoField(primary_key=True, db_column='Company_ID', serialize=False)),
                ('name', models.CharField(max_length=45, db_column='Name', blank=True)),
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
                ('ip_address', models.CharField(max_length=45, db_column='IP-address', blank=True)),
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
                ('gateway', models.ForeignKey(serialize=False, to='data_analysis.Gateway', primary_key=True, db_column='Gateway_ID')),
                ('attribute', models.CharField(max_length=45, db_column='Attribute', unique=True)),
                ('value', models.CharField(max_length=200, db_column='Value', blank=True)),
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
                ('name', models.CharField(max_length=45, db_column='Name', blank=True)),
                ('storage_on_remote', models.BooleanField(db_column='Storage_On_Remote', default=1)),
                ('remote_database_id', models.IntegerField(null=True, db_column='Remote_Database_ID', blank=True)),
                ('company', models.ForeignKey(db_column='Company_ID', to='data_analysis.Company')),
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
                ('value', models.DecimalField(null=True, db_column='Value', max_digits=10, decimal_places=5, blank=True)),
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
                ('measurementTypeID', models.AutoField(primary_key=True, db_column='MeasurementTypeID', serialize=False)),
                ('unit', models.CharField(max_length=45, db_column='Unit', blank=True)),
                ('scalar', models.IntegerField(null=True, db_column='Scalar', blank=True)),
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
                ('remote_database_id', models.AutoField(primary_key=True, db_column='Remote_Database_ID', serialize=False)),
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
                ('sensor_id', models.AutoField(primary_key=True, db_column='Sensor_ID', serialize=False)),
                ('name', models.CharField(max_length=45, db_column='Name', blank=True)),
                ('position_long', models.DecimalField(null=True, db_column='Position_Long', max_digits=10, decimal_places=0, blank=True)),
                ('position_lat', models.DecimalField(null=True, db_column='Position_Lat', max_digits=10, decimal_places=0, blank=True)),
                ('gateway', models.ForeignKey(db_column='Gateway_ID', to='data_analysis.Gateway')),
            ],
            options={
                'db_table': 'Sensor',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='measurement',
            name='measurement_type',
            field=models.ForeignKey(db_column='Measurement_Type', to='data_analysis.MeasurementType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='measurement',
            name='sensor_id',
            field=models.ForeignKey(db_column='Sensor_ID', to='data_analysis.Sensor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gateway',
            name='installation',
            field=models.ForeignKey(blank=True, to='data_analysis.Installation', null=True, db_column='Installation_ID'),
            preserve_default=True,
        ),
    ]
