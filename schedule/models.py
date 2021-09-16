import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from model_utils import Choices


class Schedule(models.Model):
    SCHEDULE_CHOICES = Choices(
        ('opened', '수업개설'),
        ('scheduled', '예약완료'),
    )
    coach = models.ForeignKey(
        'users.CoachProfile',
        on_delete=models.CASCADE,
        verbose_name='코치'
    )
    trainee = models.OneToOneField(
        'users.TraineeProfile',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='트레이니'
    )
    schedule_status = models.CharField(
        choices=SCHEDULE_CHOICES,
        default=SCHEDULE_CHOICES.opened,
        max_length=30,
        verbose_name='예약 상태'
    )
    date = models.DateField(
        verbose_name='수업일자'
    )
    time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        verbose_name='수업시간(30분_단위)'
    )


class RescheduleRequest(models.Model):
    RESCHEDULE_CHOICES = Choices(
        ('reschedule_request', '수업변경 요청'),
        ('reschedule_approval', '변경요청 승인'),
        ('reschedule_refusal', '변경요청 거부')
    )
    coach = models.ForeignKey(
        'users.CoachProfile',
        on_delete=models.CASCADE,
        verbose_name='코치'
    )
    trainee = models.OneToOneField(
        'users.TraineeProfile',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='트레이니'
    )
    reschedule = models.CharField(
        choices=RESCHEDULE_CHOICES,
        default=RESCHEDULE_CHOICES.reschedule_request,
        max_length=30,
        verbose_name='변경 상태'
    )
    reason = models.TextField(
        verbose_name='변경사유'
    )
    origin_date = models.DateField(
        verbose_name='기존수업 일자'
    )
    origin_start_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        default=0
    )
    origin_end_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        default=0
    )
    update_date = models.DateField(
        verbose_name='변경요청 일자'
    )
    update_start_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        default=0
    )
    update_end_time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        default=0
    )
    pub_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='변경요청 시간'
    )
    fixed_datetime = models.DateTimeField(
        auto_now=True,
        verbose_name='요청응답 시간'
    )

