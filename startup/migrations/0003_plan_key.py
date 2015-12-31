# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startup', '0002_auto_20151108_0221'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='key',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
