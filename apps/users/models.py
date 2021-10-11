import os
from datetime import date, timedelta

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit

from model_utils import Choices


def set_img_path(instance, filename):
    ext = os.path.splitext(filename)[-1].lower()
    file_path = f'profile/{instance.user_type}/{instance.nickname}{ext}'
    return file_path


class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('이메일은 필수입니다.')
        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)

    # 일반 유저 생성
    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', False)
        return self._create_user(email, password, **kwargs)

    # 관리자 유저 생성
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        return self._create_user(email, password, **kwargs)


class UserProfile(AbstractUser):
    OAUTH_CHOICES = Choices(
        ('Google', 'google'),
        ('default', 'default')
    )
    GENDER_CHOICES = Choices(
        ('male', '남성'),
        ('female', '여성')
    )
    USER_CHOICES = Choices(
        ('trainee', '트레이니'),
        ('coach', '코치')
    )
    email = models.EmailField(
        db_index=True,
        max_length=255,
        verbose_name='이메일'
    )
    oauth = models.OneToOneField(
        'oauth.Auth',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='OAuth'
    )
    username = models.CharField(
        max_length=150,
        verbose_name='이름'
    )
    nickname = models.CharField(
        max_length=150,
        verbose_name='닉네임'
    )
    gender = models.CharField(
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES.male,
        max_length=10,
        verbose_name='성별'
    )
    birth = models.DateField(
        validators=[
            MinValueValidator(limit_value=date(1984, 1, 1)),
            MaxValueValidator(limit_value=date.today() - timedelta(days=1))
        ],
        default=date(date.today().year - 1, 1, 1),
        verbose_name='생년월일'
    )
    profile_img = models.ImageField(
        upload_to=set_img_path,
        blank=True,
        null=True,
        verbose_name='프로필사진'
    )
    profile_thumbnail = ImageSpecField(
        source='profile_img',
        processors=[ResizeToFit(400, 400)],
        format='PNG',
        options={'quality': 80}
    )
    user_type = models.CharField(
        choices=USER_CHOICES,
        default=USER_CHOICES.trainee,
        max_length=10,
        verbose_name='회원종류'
    )
    trainee = models.OneToOneField(
        'TraineeProfile',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='트레이니 프로필'
    )
    coach = models.OneToOneField(
        'CoachProfile',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='트레이너 프로필'
    )

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'user_profile'
        verbose_name = '회원'
        verbose_name_plural = verbose_name
        ordering = ['date_joined']

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return True


class TraineeProfile(models.Model):
    purpose = models.ManyToManyField(
        'tags.HashTag',
        through="tags.PurposeTag",
    )

    class Meta:
        db_table = 'trainee_profile'
        verbose_name = '트레이니'
        verbose_name_plural = verbose_name


class CoachProfile(models.Model):
    specialty = models.ManyToManyField(
        'tags.HashTag',
        through='tags.SpecialtyTag',
    )
    years_career = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    license = models.JSONField(
        default=list,
        null=True,
        blank=True,
        verbose_name='자격증'
    )
    education = models.TextField()
    center = models.ForeignKey(
        'centers.Center',
        related_name='coach_profile',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        db_table = 'coach_profile'
        verbose_name = '코치'
        verbose_name_plural = verbose_name


class BodyInfo(models.Model):
    BODY_TYPE_CHOICES = Choices(
        ('inverted_triangle', '역삼각형'),
        ('triangle', '삼각형'),
        ('leanRectangle', '빼빼로형'),
        ('wideRectangle', '통나무형'),
        ('oval', '복부비만'),
        ('default', '없음')
    )
    trainee = models.ForeignKey(
        'TraineeProfile',
        on_delete=models.CASCADE,
        related_name='body_info',
        null=True
    )
    body_type = models.CharField(
        choices=BODY_TYPE_CHOICES,
        default=BODY_TYPE_CHOICES.default,
        max_length=20,
        verbose_name='체형'
    )
    weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='키'
    )
    height = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name='몸무게'
    )
    created_at = models.DateField(
        auto_now_add=True,
        blank=True,
        null=True
    )

    class Meta:
        db_table = 'body_info'
        verbose_name = '체형정보'
        verbose_name_plural = verbose_name
        get_latest_by = ['created_at']
