# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startup', '0006_plan_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='source',
            field=models.ForeignKey(blank=True, to='startup.City', null=True),
            preserve_default=True,
        ),
    ]
