# Generated by Django 3.2.5 on 2021-09-19 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('programs', '0004_auto_20210918_1548'),
        ('quests', '0004_rename_service_quest_program'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mealplanner',
            name='breakfast',
            field=models.JSONField(default=list, verbose_name='아침'),
        ),
        migrations.AlterField(
            model_name='mealplanner',
            name='dinner',
            field=models.JSONField(default=list, verbose_name='저녁'),
        ),
        migrations.AlterField(
            model_name='mealplanner',
            name='lunch',
            field=models.JSONField(default=list, verbose_name='점심'),
        ),
        migrations.AlterField(
            model_name='quest',
            name='program',
            field=models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='programs.program', verbose_name='프로그램'),
        ),
        migrations.AlterField(
            model_name='workout',
            name='workout_content',
            field=models.JSONField(default=list, verbose_name='운동퀘스트'),
        ),
    ]
