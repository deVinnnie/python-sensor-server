# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_analysis', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorconfiguration',
            name='attribute',
            field=models.CharField(max_length=45, serialize=False, primary_key=True),
            preserve_default=True,
        ),
    ]
