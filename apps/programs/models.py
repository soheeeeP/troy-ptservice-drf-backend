from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from utils.models import TimeStampedModel


class Program(TimeStampedModel):
    coach = models.ForeignKey(
        'users.CoachProfile',
        on_delete=models.CASCADE,
        verbose_name='코치'
    )
    trainee = models.ForeignKey(
        'users.TraineeProfile',
        on_delete=models.CASCADE,
        verbose_name='트레이니'
    )
    evaluation = models.OneToOneField(
        'Evaluation',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='평가'
    )

    class Meta:
        db_table = 'program'
        verbose_name = "프로그램"
        verbose_name_plural = verbose_name
        get_latest_by = ['created_at']


class OfflineClass(TimeStampedModel):
    program = models.ForeignKey(
        'Program',
        on_delete=models.CASCADE,
        verbose_name='서비스'
    )
    class_contents = models.TextField()

    class Meta:
        db_table = 'offline_class'
        verbose_name = "오프라인 수업"
        verbose_name_plural = verbose_name
        get_latest_by = ['created_at']


class Evaluation(TimeStampedModel):
    communication = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name='커뮤니케이션 만족도'
    )
    care = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name='서비스 만족도'
    )
    total_rate = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)],
        verbose_name='종합 추천도'
    )
    text = models.TextField(
        null=True,
        verbose_name='텍스트 평가'
    )

    class Meta:
        db_table = 'evaluation'
        verbose_name = "평가"
        verbose_name_plural = verbose_name
