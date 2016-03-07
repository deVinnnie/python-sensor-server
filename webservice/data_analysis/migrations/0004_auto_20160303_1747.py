# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_analysis', '0003_auto_20160229_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='measurement',
            name='value',
            field=models.FloatField(null=True, blank=True, db_column='Value'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensor',
            name='name',
            field=models.CharField(default='Sensor Node', max_length=45, blank=True, db_column='Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensor',
            name='sensor_id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='Sensor_ID'),
            preserve_default=True,
        ),
    ]
