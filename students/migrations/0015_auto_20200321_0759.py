# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('students', '0014_auto_20200317_1334'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='exam',
            name='data_and_time',
        ),
        migrations.AddField(
            model_name='exam',
            name='data',
            field=models.DateField(null=True, verbose_name='Data'),
        ),
    ]
