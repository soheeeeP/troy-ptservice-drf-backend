from django.db import models


class HashTag(models.Model):
    SPECIALTY = 'specialty'
    PURPOSE = 'purpose'
    GOAL = 'goal'
    TAG_CHOICES = [
        (SPECIALTY, '전문성'),
        (PURPOSE, '목적'),
        (GOAL, '목표')
    ]
    tag_type = models.CharField(
        choices=TAG_CHOICES,
        default=GOAL,
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
    trainer = models.ForeignKey(
        "users.TrainerProfile",
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


class GoalTag(models.Model):
    goal = models.ForeignKey(
        "services.Goal",
        on_delete=models.CASCADE
    )
    tag = models.ForeignKey(
        'HashTag',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'goal_tag'
        verbose_name = '목표 태그'
        verbose_name_plural = verbose_name
