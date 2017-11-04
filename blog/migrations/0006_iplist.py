# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-02 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_remove_links_date_publish'),
    ]

    operations = [
        migrations.CreateModel(
            name='Iplist',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20)),
                ('time', models.TimeField(default=1509615725.735588)),
            ],
            options={
                'verbose_name': 'ip访问时间',
                'verbose_name_plural': 'ip访问时间',
            },
        ),
    ]