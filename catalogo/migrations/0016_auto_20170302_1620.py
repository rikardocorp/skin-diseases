# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-02 21:20
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogo', '0015_auto_20170121_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Commentuser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(default=datetime.datetime(2017, 3, 2, 21, 20, 24, 660775, tzinfo=utc))),
            ],
        ),
        migrations.AlterField(
            model_name='category',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 2, 21, 20, 24, 658838, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='commentimage',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 2, 21, 20, 24, 660303, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='commentimage',
            name='text',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='disease',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 2, 21, 20, 24, 659272, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='imageskin',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 2, 21, 20, 24, 659782, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='sourcedata',
            name='pub_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 3, 2, 21, 20, 24, 658425, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='commentuser',
            name='commentimage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalogo.Commentimage'),
        ),
        migrations.AddField(
            model_name='commentuser',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]