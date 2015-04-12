# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_profile_nickname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='author',
            field=models.OneToOneField(to='core.Profile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='question',
            name='author',
            field=models.OneToOneField(to='core.Profile'),
            preserve_default=True,
        ),
    ]
