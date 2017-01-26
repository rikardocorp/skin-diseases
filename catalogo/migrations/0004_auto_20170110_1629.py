# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-10 16:29
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0003_auto_20170110_0434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 10, 16, 29, 19, 762553, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='disease',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 10, 16, 29, 19, 762943, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='imageskin',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 10, 16, 29, 19, 763441, tzinfo=utc)),
        ),
    ]