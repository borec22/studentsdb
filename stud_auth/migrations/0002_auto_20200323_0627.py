# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stud_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='stprofile',
            name='address',
            field=models.CharField(default=b'', max_length=30, verbose_name='Adress', blank=True),
        ),
        migrations.AddField(
            model_name='stprofile',
            name='pasport_number',
            field=models.CharField(default=b'', max_length=10, verbose_name='Pasport Number', blank=True),
        ),
        migrations.AddField(
            model_name='stprofile',
            name='photo',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='\u0424\u043e\u0442\u043e', blank=True),
        ),
    ]
