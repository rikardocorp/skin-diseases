# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-17 07:36
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('catalogo', '0008_auto_20170117_0030'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 17, 7, 36, 12, 458704, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='disease',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 17, 7, 36, 12, 459117, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='imageskin',
            name='description',
            field=models.CharField(default='', max_length=1000),
        ),
        migrations.AlterField(
            model_name='imageskin',
            name='docfile',
            field=models.FileField(blank=True, null=True, upload_to='unknown/'),
        ),
        migrations.AlterField(
            model_name='imageskin',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 17, 7, 36, 12, 459835, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sourcedata',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 17, 7, 36, 12, 458252, tzinfo=utc)),
        ),
    ]