# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 04:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 10, 4, 28, 18, 294688)),
        ),
        migrations.AddField(
            model_name='disease',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 10, 4, 28, 18, 295122)),
        ),
        migrations.AddField(
            model_name='imageskin',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 10, 4, 28, 18, 295612)),
        ),
    ]
