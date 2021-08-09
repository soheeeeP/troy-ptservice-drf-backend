# Generated by Django 3.2.5 on 2021-08-01 07:09

import django.contrib.auth.models
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # ('centers', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_type', models.CharField(max_length=20, verbose_name='체형')),
                ('weight', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='키')),
                ('height', models.DecimalField(decimal_places=2, max_digits=5, verbose_name='몸무게')),
            ],
            options={
                'verbose_name': 'bodyinfo',
                'verbose_name_plural': 'bodyinfo',
                'db_table': '체형정보',
            },
        ),
        migrations.CreateModel(
            name='TrainerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('years_career', models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)])),
                ('license', models.BooleanField(default=False)),
                ('education', models.TextField()),
                # ('center', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainer_profile', to='centers.center')),
            ],
            options={
                'verbose_name': '트레이니',
                'verbose_name_plural': '트레이니',
                'db_table': 'trainer_profile',
            },
        ),
        migrations.CreateModel(
            name='TraineeProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainee_profile', to='users.bodyinfo')),
            ],
            options={
                'verbose_name': '트레이너',
                'verbose_name_plural': '트레이너',
                'db_table': 'trainee_profile',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='이메일')),
                ('username', models.CharField(max_length=150, verbose_name='이름')),
                ('nickname', models.CharField(max_length=150, unique=True, verbose_name='닉네임')),
                ('gender', models.CharField(choices=[('male', '남성'), ('female', '여성')], default='male', max_length=10, verbose_name='성별')),
                ('birth_year', models.IntegerField(choices=[(1984, 1984), (1985, 1985), (1986, 1986), (1987, 1987), (1988, 1988), (1989, 1989), (1990, 1990), (1991, 1991), (1992, 1992), (1993, 1993), (1994, 1994), (1995, 1995), (1996, 1996), (1997, 1997), (1998, 1998), (1999, 1999), (2000, 2000), (2001, 2001), (2002, 2002), (2003, 2003), (2004, 2004), (2005, 2005), (2006, 2006), (2007, 2007), (2008, 2008), (2009, 2009), (2010, 2010), (2011, 2011), (2012, 2012), (2013, 2013), (2014, 2014), (2015, 2015), (2016, 2016), (2017, 2017), (2018, 2018), (2019, 2019), (2020, 2020), (2021, 2021)], default=2021, verbose_name='생년월일')),
                ('profile_img', models.URLField(verbose_name='프로필사진')),
                ('user_type', models.CharField(choices=[('trainee', '트레이니'), ('trainer', '트레이너')], default='trainee', max_length=10, verbose_name='회원종류')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('trainee', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.traineeprofile', verbose_name='트레이니 프로필')),
                ('trainer', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.trainerprofile', verbose_name='트레이너 프로필')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '회원',
                'verbose_name_plural': '회원',
                'db_table': 'user_profile',
                'ordering': ['date_joined'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
