from django.db import models

from model_utils import Choices
from utils.models import TimeStampedModel


class Auth(models.Model):
    OAUTH_CHOICES = Choices(
        ('google', 'google'),
        ('default', 'default')
    )
    oauth_type = models.CharField(
        choices=OAUTH_CHOICES,
        default=OAUTH_CHOICES.default,
        max_length=10,
        verbose_name='OAuth_Type'
    )
    oauth_token = models.CharField(
        db_index=True,
        max_length=255,
        default='',
        verbose_name='OAuth_ID'
    )

    class Meta:
        db_table = 'auth'
        verbose_name = 'OAuth 인증'
        verbose_name_plural = verbose_name


class AuthSMS(TimeStampedModel):
    phone_number = models.CharField(
        verbose_name='휴대폰 번호',
        db_index=True,
        null=True,
        max_length=11
    )
    auth_number = models.IntegerField(
        verbose_name='인증번호',
        max_length=4
    )
    validation = models.BooleanField(
        verbose_name='인증여부',
        default=False
    )

    class Meta:
        db_table = 'auth_sms'
        verbose_name = '휴대폰 인증'
        verbose_name_plural = verbose_name
