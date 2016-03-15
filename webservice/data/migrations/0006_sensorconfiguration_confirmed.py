# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0005_alert_archived'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensorconfiguration',
            name='confirmed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
