import datetime


from tags.models import HashTag, PurposeTag, SpecialtyTag

from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinValueValidator, MaxValueValidator

from model_utils import Choices


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
    YEAR_CHOICES = [(r, r) for r in range(1984, datetime.date.today().year+1)]
    GENDER_CHOICES = Choices(
        ('male', '남성'),
        ('female', '여성')
    )
    USER_CHOICES = Choices(
        ('trainee', '트레이니'),
        ('trainer', '트레이너')
    )
    email = models.EmailField(
        unique=True,
        max_length=255,
        verbose_name='이메일'
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
    username = models.CharField(
        max_length=150,
        verbose_name='이름'
    )
    nickname = models.CharField(
        unique=True,
        max_length=150,
        verbose_name='닉네임'
    )
    gender = models.CharField(
        choices=GENDER_CHOICES,
        default=GENDER_CHOICES.male,
        max_length=10,
        verbose_name='성별'
    )
    birth_year = models.IntegerField(
        choices=YEAR_CHOICES,
        default=datetime.datetime.now().year,
        verbose_name='생년월일'
    )
    profile_img = models.FileField(
        verbose_name='프로필사진'
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
    trainer = models.OneToOneField(
        'TrainerProfile',
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


class BodyInfo(models.Model):
    body_type = models.CharField(       # choices로 구체화 필요
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

    class Meta:
        db_table = 'bodyinfo'
        verbose_name = '체형정보'
        verbose_name_plural = verbose_name


class TraineeProfile(models.Model):
    body_info = models.ForeignKey(
        'BodyInfo',
        on_delete=models.CASCADE,
        related_name='trainee_profile'
    )
    purpose = models.ManyToManyField(
        HashTag,
        through="tags.PurposeTag",
    )

    class Meta:
        db_table = 'trainee_profile'
        verbose_name = '트레이너'
        verbose_name_plural = verbose_name


class TrainerProfile(models.Model):
    specialty = models.ManyToManyField(
        HashTag,
        through='tags.SpecialtyTag',
    )
    years_career = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    license = models.BooleanField(default=False)
    education = models.TextField()
    center = models.ForeignKey(
        'centers.Center',
        related_name='trainer_profile',
        on_delete=models.CASCADE,
        null=True
    )

    class Meta:
        db_table = 'trainer_profile'
        verbose_name = '트레이니'
        verbose_name_plural = verbose_name
