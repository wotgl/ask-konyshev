# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150412_0909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.ForeignKey(to='core.Profile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.ForeignKey(to='core.Profile'),
            preserve_default=True,
        ),
    ]
