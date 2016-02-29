# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_analysis', '0002_auto_20160229_1202'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gateway',
            name='gateway_id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='Gateway_ID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='installation',
            name='installation_id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='Installation_ID'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='installation',
            name='storage_on_remote',
            field=models.IntegerField(blank=True, default=0, db_column='Storage_On_Remote'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensorconfiguration',
            name='attribute',
            field=models.CharField(primary_key=True, max_length=45),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sensorconfiguration',
            name='sensor',
            field=models.ForeignKey(to='data_analysis.Sensor', serialize=False, db_column='Sensor_ID', related_name='config', primary_key=True),
            preserve_default=True,
        ),
    ]
