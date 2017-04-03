# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-31 05:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cash', '0010_auto_20170329_1131'),
    ]

    state_operations = [
        migrations.RemoveField(
            model_name='cashtransaction',
            name='invoice',
        ),
        migrations.RemoveField(
            model_name='cashtransaction',
            name='original_txn',
        ),
        migrations.RemoveField(
            model_name='district',
            name='region',
        ),
        migrations.DeleteModel(
            name='CashTransaction',
        ),
        migrations.DeleteModel(
            name='District',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=state_operations,
        ),
    ] 