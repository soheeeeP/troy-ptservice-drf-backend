from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Program(models.Model):
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
    started_date = models.DateField(
        auto_now_add=True
    )
    finished_date = models.DateField(
        null=True
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
        get_latest_by = ['started_date']


class OfflineClass(models.Model):
    program = models.ForeignKey(
        'Program',
        on_delete=models.CASCADE,
        verbose_name='서비스'
    )
    created_at = models.DateTimeField(
        verbose_name='오프라인 수업일자'
    )
    class_contents = models.TextField()

    class Meta:
        db_table = 'offline_class'
        verbose_name = "오프라인 수업"
        verbose_name_plural = verbose_name
        get_latest_by = ['created_at']


class Evaluation(models.Model):
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
