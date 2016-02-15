# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_analysis', '0004_auto_20160212_1316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorconfiguration',
            name='attribute',
            field=models.CharField(primary_key=True, max_length=45),
            preserve_default=True,
        ),
    ]
