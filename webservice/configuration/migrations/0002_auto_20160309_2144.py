# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sensorconfiguration',
            name='id',
            field=models.AutoField(serialize=False, primary_key=True, db_column='id'),
            preserve_default=True,
        ),
    ]
