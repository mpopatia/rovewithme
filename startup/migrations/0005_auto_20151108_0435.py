# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('startup', '0004_cityinplan_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityGraph',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('weight', models.IntegerField(default=0)),
                ('one', models.ForeignKey(related_name='one', to='startup.City')),
                ('two', models.ForeignKey(related_name='two', to='startup.City')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='plan',
            name='key',
            field=models.CharField(max_length=200, unique=True, null=True, blank=True),
            preserve_default=True,
        ),
    ]
