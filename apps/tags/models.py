from django.db import models
from model_utils import Choices


class HashTag(models.Model):
    TAG_CHOICES = Choices(
        ('default', 'default'),
        ('specialty', '전문성'),
        ('purpose', '목적')
    )
    tag_type = models.CharField(
        choices=TAG_CHOICES,
        default=TAG_CHOICES.default,
        max_length=20,
        verbose_name='태그 종류'
    )
    tag_content = models.CharField(
        max_length=20,
        verbose_name='태그 이름'
    )

    class Meta:
        db_table = 'hash_tag'
        verbose_name = '해시태그'
        verbose_name_plural = verbose_name


class SpecialtyTag(models.Model):
    coach = models.ForeignKey(
        "users.CoachProfile",
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        'HashTag',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'specialty_tag'
        verbose_name = '전문성 태그'
        verbose_name_plural = verbose_name


class PurposeTag(models.Model):
    trainee = models.ForeignKey(
        "users.TraineeProfile",
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        'HashTag',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'purpose_tag'
        verbose_name = '목적 태그'
        verbose_name_plural = verbose_name
