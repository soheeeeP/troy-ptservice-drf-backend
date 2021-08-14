import datetime

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from model_utils import Choices


class TrainerSchedule(models.Model):
    DAY_OF_WEEK_CHOICES = Choices(
        (0, 'Monday', '월요일'),
        (1, 'Tuesday', '화요일'),
        (2, 'Wednesday', '수요일'),
        (3, 'Thursday', '목요일'),
        (4, 'Friday', '금요일'),
        (5, 'Saturday', '토요일'),
        (6, 'Sunday', '일요일')
    )
    trainer = models.ForeignKey(
        'users.TrainerProfile',
        on_delete=models.CASCADE,
        verbose_name='트레이너'
    )
    trainee = models.OneToOneField(
        'users.TraineeProfile',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='트레이니'
    )
    date = models.DateField(
        verbose_name='수업일자'
    )
    day_of_week = models.CharField(
        choices=DAY_OF_WEEK_CHOICES,
        default=DAY_OF_WEEK_CHOICES.Monday,
        max_length=10,
        verbose_name='수업요일'
    )
    time = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        verbose_name='수업시간(30분_단위)'
    )
    reserved = models.BooleanField(
        default=False,
        verbose_name='예약여부'
    )


class RescheduleRequest(models.Model):
    trainer = models.ForeignKey(
        'users.TrainerProfile',
        on_delete=models.CASCADE,
        verbose_name='트레이너'
    )
    trainee = models.OneToOneField(
        'users.TraineeProfile',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='트레이니'
    )
    reason = models.TextField(
        verbose_name='변경사유'
    )
    origin_date = models.DateField(
        verbose_name='기존수업 일자'
    )
    update_date = models.DateField(
        verbose_name='변경요청 일자'
    )
    requested_datetime = models.DateTimeField(
        auto_now_add=True,
        verbose_name='변경요청 시간'
    )
    fixed_date = models.DateTimeField(
        auto_now=True,
        verbose_name='요청승인 시간'
    )
    approval = models.BooleanField(
        default=False,
        verbose_name='승인여부'
    )
