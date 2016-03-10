# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='GatewayConfiguration',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('attribute', models.CharField(db_column='Attribute', max_length=45)),
                ('value', models.CharField(blank=True, db_column='Value', max_length=200)),
                ('gateway', models.ForeignKey(db_column='Gateway_ID', to='data.Gateway', related_name='config')),
            ],
            options={
                'managed': True,
                'db_table': 'Gateway_Configuration',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SensorConfiguration',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('attribute', models.CharField(db_column='Attribute', max_length=45)),
                ('value', models.CharField(blank=True, db_column='Value', max_length=200)),
                ('sensor', models.ForeignKey(db_column='Sensor_ID', to='data.Sensor', related_name='config')),
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
        migrations.AlterUniqueTogether(
            name='gatewayconfiguration',
            unique_together=set([('gateway', 'attribute')]),
        ),
    ]
