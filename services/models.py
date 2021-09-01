from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Service(models.Model):
    trainer = models.ForeignKey(
        'users.TrainerProfile',
        on_delete=models.CASCADE,
        verbose_name='트레이너'
    )
    trainee = models.ForeignKey(
        'users.TraineeProfile',
        on_delete=models.CASCADE,
        verbose_name='트레이니'
    )
    start_date = models.DateField(
        auto_now_add=True
    )
    end_date = models.DateField(
        null=True
    )

    class Meta:
        db_table = 'service'
        verbose_name = "서비스"
        verbose_name_plural = verbose_name
        get_latest_by = ['start_date']


class OnlineService(models.Model):
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        verbose_name='서비스'
    )
    evaluation = models.OneToOneField(
        'Evaluation',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='평가'
    )
    start_date = models.DateField()
    end_date = models.DateField()
    goal = models.OneToOneField(
        'Goal',
        on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'online_service'
        verbose_name = "온라인 서비스"
        verbose_name_plural = verbose_name
        get_latest_by = ['start_date']


class OfflineService(models.Model):
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        verbose_name='서비스'
    )
    date = models.DateTimeField(
        verbose_name='오프라인 수업일자'
    )
    class_contents = models.TextField()

    class Meta:
        db_table = 'offline_service'
        verbose_name = "오프라인 서비스"
        verbose_name_plural = verbose_name


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


class Goal(models.Model):
    due_date = models.DateField()
    text_goal = models.CharField(
        max_length=20
    )

    class Meta:
        db_table = 'goal'
        verbose_name = "목표"
        verbose_name_plural = verbose_name
