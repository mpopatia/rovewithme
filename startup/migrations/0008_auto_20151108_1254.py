# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startup', '0007_plan_source'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airport',
            name='code',
            field=models.CharField(unique=True, max_length=4000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='airport',
            name='name',
            field=models.CharField(max_length=2000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='city',
            name='city',
            field=models.CharField(max_length=2000),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='city',
            name='state',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='plan',
            name='key',
            field=models.CharField(max_length=2000, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
