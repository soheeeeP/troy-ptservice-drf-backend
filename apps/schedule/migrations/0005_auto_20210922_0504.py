# Generated by Django 3.2.5 on 2021-09-22 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_alter_reschedulerequest_fixed_datetime'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reschedulerequest',
            old_name='pub_datetime',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='reschedulerequest',
            old_name='fixed_datetime',
            new_name='fixed_at',
        ),
    ]
