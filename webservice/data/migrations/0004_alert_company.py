# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0003_auto_20160315_1246'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='company',
            field=models.ForeignKey(default=1, related_name='alerts', to='data.Company'),
            preserve_default=False,
        ),
    ]
