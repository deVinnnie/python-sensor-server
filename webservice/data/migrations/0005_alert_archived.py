# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_alert_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='archived',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
