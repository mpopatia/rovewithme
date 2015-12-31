# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startup', '0005_auto_20151108_0435'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='budget',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
    ]
