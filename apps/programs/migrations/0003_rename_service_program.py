# Generated by Django 3.2.5 on 2021-09-18 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quests', '0003_auto_20210913_1412'),
        ('users', '0001_initial'),
        ('programs', '0002_auto_20210913_0722'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Service',
            new_name='Program',
        ),
    ]