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
                ('permission_id', models.IntegerField(primary_key=True, serialize=False, db_column='Permission_ID')),
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
            name='Role',
            fields=[
                ('role_id', models.IntegerField(primary_key=True, serialize=False, db_column='Role_ID')),
                ('role_name', models.CharField(max_length=45, db_column='Role_Name')),
            ],
            options={
                'db_table': 'Role',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RoleHasPermission',
            fields=[
                ('role', models.ForeignKey(serialize=False, db_column='Role_ID', to='data_analysis.Role', primary_key=True)),
                ('permission', models.ForeignKey(db_column='Permission_ID', to='data_analysis.Permission', primary_key=True)),
            ],
            options={
                'db_table': 'Role_has_Permission',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False, db_column='User_ID')),
                ('username', models.CharField(max_length=45, db_column='Username')),
                ('password', models.CharField(max_length=45, db_column='Password')),
                ('email', models.CharField(max_length=300, db_column='Email')),
                ('full_name', models.CharField(max_length=300, db_column='Full_Name')),
            ],
            options={
                'db_table': 'User',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserHasPermission',
            fields=[
                ('user', models.ForeignKey(serialize=False, db_column='User_ID', to='data_analysis.User', primary_key=True)),
                ('permission', models.ForeignKey(db_column='Permission_ID', to='data_analysis.Permission', primary_key=True)),
            ],
            options={
                'db_table': 'User_has_Permission',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserHasRole',
            fields=[
                ('user', models.ForeignKey(serialize=False, db_column='User_ID', to='data_analysis.User', primary_key=True)),
                ('role', models.ForeignKey(db_column='Role_ID', to='data_analysis.Role', primary_key=True)),
            ],
            options={
                'db_table': 'User_has_Role',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('company_id', models.IntegerField(primary_key=True, serialize=False, db_column='Company_ID')),
                ('name', models.CharField(max_length=45, blank=True, db_column='Name')),
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
                ('gateway_id', models.IntegerField(primary_key=True, serialize=False, db_column='Gateway_ID')),
                ('ip_address', models.CharField(max_length=45, blank=True, db_column='IP-address')),
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
                ('gateway', models.ForeignKey(serialize=False, db_column='Gateway_ID', to='data_analysis.Gateway', primary_key=True)),
                ('attribute', models.CharField(max_length=45, primary_key=True, db_column='Attribute')),
                ('value', models.CharField(max_length=200, blank=True, db_column='Value')),
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
                ('installation_id', models.IntegerField(primary_key=True, serialize=False, db_column='Installation_ID')),
                ('name', models.CharField(max_length=45, blank=True, db_column='Name')),
                ('storage_on_remote', models.IntegerField(db_column='Storage_On_Remote')),
                ('remote_database_id', models.IntegerField(blank=True, null=True, db_column='Remote_Database_ID')),
                ('company', models.ForeignKey(to='data_analysis.Company', db_column='Company_ID')),
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
                ('measurement_id', models.IntegerField(primary_key=True, serialize=False, db_column='Measurement_ID')),
                ('timestamp', models.DateTimeField(db_column='Timestamp')),
                ('sensor_id', models.IntegerField(db_column='Sensor_ID')),
                ('measurement_type', models.IntegerField(db_column='Measurement_Type')),
                ('value', models.DecimalField(blank=True, decimal_places=5, max_digits=10, null=True, db_column='Value')),
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
                ('unit', models.CharField(max_length=45, blank=True, db_column='Unit')),
                ('scalar', models.IntegerField(blank=True, null=True, db_column='Scalar')),
                ('name', models.CharField(max_length=45, blank=True, db_column='Name')),
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
                ('url', models.CharField(max_length=300, blank=True, db_column='URL')),
                ('username', models.CharField(max_length=45, blank=True, db_column='Username')),
                ('password', models.CharField(max_length=45, blank=True, db_column='Password')),
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
                ('sensor_id', models.IntegerField(primary_key=True, serialize=False, db_column='Sensor_ID')),
                ('name', models.CharField(max_length=45, blank=True, db_column='Name')),
                ('position_long', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, db_column='Position_Long')),
                ('position_lat', models.DecimalField(blank=True, decimal_places=0, max_digits=10, null=True, db_column='Position_Lat')),
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
                ('sensor', models.ForeignKey(serialize=False, db_column='Sensor_ID', to='data_analysis.Sensor', primary_key=True)),
                ('attribute', models.CharField(max_length=45, primary_key=True)),
                ('value', models.CharField(max_length=200, blank=True, db_column='Value')),
            ],
            options={
                'db_table': 'Sensor_Configuration',
                'managed': True,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sensor',
            name='gateway',
            field=models.ForeignKey(to='data_analysis.Gateway', db_column='Gateway_ID'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='gateway',
            name='installation',
            field=models.ForeignKey(null=True, to='data_analysis.Installation', blank=True, db_column='Installation_ID'),
            preserve_default=True,
        ),
    ]
