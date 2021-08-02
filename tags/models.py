from django.db import models

# Create your models here.
class HashTag(models.Model):
    tag_type = models.CharField(
        max_length = 20,
        verbose_name = '태그 종류'
    )
    tag_content = models.CharField(
        max_length = 20,
        verbose_name= '태그 이름'
    )

    class Meta:
        db_table = 'hash_tag'
        verbose_name = '해시태그'
        verbose_name_plural = verbose_name

class SpecialtyTag(models.Model):
    trainer_id = models.ForeignKey(
        'TrainerProfile',
        on_delete = models.CASCADE
    )
    tag_id = models.ForeignKey(
        'HashTag',
        on_delete = models.CASCADE
    )

    class Meta:
        db_table = 'specialty_tag'
        verbose_name = '전문성 태그'
        verbose_name_plural = verbose_name

class PurposeTag(models.Model):
    trainee_id = models.ForeignKey(
        'TraineeProfile',
        on_delete = models.CASCADE
    )
    tag_id = models.ForeignKey(
        'HashTag',
        on_delete = models.CASCADE
    )

    class Meta:
        db_table = 'purpose_tag'
        verbose_name = '목적 태그'
        verbose_name_plural = verbose_name

class GoalTag(models.Model):
    goal_id = models.ForeignKey(
        'Goal',
        on_delete = models.CASCADE
    )
    tag_id = models.ForeignKey(
        'HashTag',
        on_delete = models.CASCADE
    )

    class Meta:
        db_table = 'goal_tag'
        verbose_name = '목표 태그'
        verbose_name_plural = verbose_name