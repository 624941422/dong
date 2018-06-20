# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20180609_2349'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='qq',
            field=models.CharField(verbose_name='QQ', max_length=64, unique=True),
        ),
    ]
