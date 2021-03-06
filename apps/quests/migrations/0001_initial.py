# Generated by Django 3.2.5 on 2021-09-13 07:24

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('programs', '0002_auto_20210913_0722'),
    ]

    operations = [
        migrations.CreateModel(
            name='MealPlanner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('breakfast', models.CharField(max_length=255, verbose_name='아침')),
                ('breakfast_clear', models.BooleanField(default=False, verbose_name='아침퀘스트 달성여부')),
                ('lunch', models.CharField(max_length=255, verbose_name='점심')),
                ('lunch_clear', models.BooleanField(default=False, verbose_name='아침퀘스트 달성여부')),
                ('dinner', models.CharField(max_length=255, verbose_name='저녁')),
                ('dinner_clear', models.BooleanField(default=False, verbose_name='아침퀘스트 달성여부')),
            ],
            options={
                'verbose_name': '식단',
                'verbose_name_plural': '식단',
                'db_table': 'meal_planner',
            },
        ),
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_score', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, verbose_name='식단 달성률')),
                ('workout_score', models.DecimalField(decimal_places=2, default=0.0, max_digits=4, verbose_name='운동 달성률')),
            ],
            options={
                'verbose_name': '달성률',
                'verbose_name_plural': '달성률',
                'db_table': 'score',
            },
        ),
        migrations.CreateModel(
            name='Workout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('workout_content', models.TextField(verbose_name='운동퀘스트')),
                ('workout_clear', models.BooleanField(default=False, verbose_name='운동퀘스트 달성여부')),
            ],
            options={
                'verbose_name': '운동',
                'verbose_name_plural': '운동',
                'db_table': 'workout',
            },
        ),
        migrations.CreateModel(
            name='Quest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True, verbose_name='퀘스트 생성일자')),
                ('rate_feedback', models.PositiveSmallIntegerField(default=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='스탬프')),
                ('quest_feedback', models.TextField(default='', null=True, verbose_name='피드백')),
                ('meal_planner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quests.mealplanner', verbose_name='식단퀘스트')),
                ('quest_score', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='quests.score', verbose_name='퀘스트 달성률')),
                ('service', models.ForeignKey(default=True, on_delete=django.db.models.deletion.CASCADE, to='programs.service', verbose_name='서비스')),
                ('workout', models.ManyToManyField(to='quests.Workout', verbose_name='운동퀘스트')),
            ],
            options={
                'verbose_name': '퀘스트',
                'verbose_name_plural': '퀘스트',
                'db_table': 'quest',
            },
        ),
    ]
