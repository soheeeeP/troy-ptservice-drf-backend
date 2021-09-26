# Generated by Django 3.2.5 on 2021-09-22 05:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0004_auto_20210918_1548'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Class',
            new_name='OfflineClass',
        ),
        migrations.AlterModelOptions(
            name='offlineclass',
            options={'get_latest_by': ['created_at'], 'verbose_name': '오프라인 수업', 'verbose_name_plural': '오프라인 수업'},
        ),
        migrations.AlterModelOptions(
            name='program',
            options={'get_latest_by': ['started_date'], 'verbose_name': '프로그램', 'verbose_name_plural': '프로그램'},
        ),
        migrations.RenameField(
            model_name='offlineclass',
            old_name='date',
            new_name='created_at',
        ),
        migrations.RenameField(
            model_name='program',
            old_name='end_date',
            new_name='finished_date',
        ),
        migrations.RenameField(
            model_name='program',
            old_name='start_date',
            new_name='started_date',
        ),
        migrations.AlterModelTable(
            name='offlineclass',
            table='offline_class',
        ),
    ]
