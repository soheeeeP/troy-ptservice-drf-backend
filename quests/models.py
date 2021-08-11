import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Quest(models.Model):
    online_service = models.ForeignKey(
        "services.OnlineService",
        on_delete=models.CASCADE,
        default=True,
        verbose_name='온라인 서비스'
    )
    date = models.DateTimeField(
        auto_now=True,
        verbose_name='퀘스트 생성일자'
    )
    meal_planner = models.OneToOneField(
        'MealPlanner',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='식단퀘스트'
    )
    workout = models.ManyToManyField(
        'Workout',
        verbose_name='운동퀘스트',

    )
    rate_feedback = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        default=3,
        verbose_name='스탬프',
        blank=False
    )
    quest_feedback = models.TextField(
        default='',
        verbose_name='피드백',
        null=True
    )

    class Meta:
        db_table = 'quest'
        verbose_name = '퀘스트'
        verbose_name_plural = verbose_name


class MealPlanner(models.Model):
    breakfast = models.CharField(
        max_length=255,
        verbose_name='아침'
    )
    breakfast_clear = models.BooleanField(
        default=False,
        verbose_name='아침퀘스트 달성여부'
    )
    lunch = models.CharField(
        max_length=255,
        verbose_name='점심'
    )
    lunch_clear = models.BooleanField(
        default=False,
        verbose_name='아침퀘스트 달성여부'
    )
    dinner = models.CharField(
        max_length=255,
        verbose_name='저녁'
    )
    dinner_clear = models.BooleanField(
        default=False,
        verbose_name='아침퀘스트 달성여부'
    )

    class Meta:
        db_table = 'meal_planner'
        verbose_name = '식단'
        verbose_name_plural = verbose_name


class Workout(models.Model):
    workout_content = models.TextField(verbose_name='운동퀘스트')
    workout_clear = models.BooleanField(
        default=False,
        verbose_name='운동퀘스트 달성여부'
    )

    class Meta:
        db_table = 'workout'
        verbose_name = '운동'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.workout_content}[:20]...'
