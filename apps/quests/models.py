import datetime

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Quest(models.Model):
    program = models.ForeignKey(
        "programs.Program",
        on_delete=models.CASCADE,
        default=True,
        verbose_name='프로그램'
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name='퀘스트 생성일자'
    )
    meal_planner = models.OneToOneField(
        'MealPlanner',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='식단퀘스트'
    )
    workout = models.OneToOneField(
        'Workout',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='운동퀘스트'
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
    meal_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.0,
        verbose_name='식단 달성률'
    )
    workout_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=0.0,
        verbose_name='운동 달성률'
    )

    class Meta:
        db_table = 'quest'
        verbose_name = '퀘스트'
        verbose_name_plural = verbose_name


class MealPlanner(models.Model):
    breakfast = models.JSONField(
        default=list,
        verbose_name='아침'
    )
    lunch = models.JSONField(
        default=list,
        verbose_name='점심'
    )
    dinner = models.JSONField(
        default=list,
        verbose_name='저녁'
    )

    class Meta:
        db_table = 'meal_planner'
        verbose_name = '식단'
        verbose_name_plural = verbose_name


class Workout(models.Model):
    workout_content = models.JSONField(
        default=list,
        verbose_name='운동퀘스트'
    )

    class Meta:
        db_table = 'workout'
        verbose_name = '운동'
        verbose_name_plural = verbose_name

    def __str__(self):
        return f'{self.workout_content}[:20]...'

