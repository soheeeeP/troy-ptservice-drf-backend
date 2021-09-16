# Generated by Django 3.2.5 on 2021-09-13 06:52

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Evaluation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('communication', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='커뮤니케이션 만족도')),
                ('care', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='서비스 만족도')),
                ('total_rate', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)], verbose_name='종합 추천도')),
                ('text', models.TextField(null=True, verbose_name='텍스트 평가')),
            ],
            options={
                'verbose_name': '평가',
                'verbose_name_plural': '평가',
                'db_table': 'evaluation',
            },
        ),
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateField()),
                ('text_goal', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': '목표',
                'verbose_name_plural': '목표',
                'db_table': 'goal',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(null=True)),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.coachprofile', verbose_name='코치')),
                ('evaluation', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='services.evaluation', verbose_name='평가')),
                ('goal', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='services.goal', verbose_name='목표')),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.traineeprofile', verbose_name='트레이니')),
            ],
            options={
                'verbose_name': '서비스',
                'verbose_name_plural': '서비스',
                'db_table': 'service',
                'get_latest_by': ['start_date'],
            },
        ),
        migrations.CreateModel(
            name='Class',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='오프라인 수업일자')),
                ('class_contents', models.TextField()),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service', verbose_name='서비스')),
            ],
            options={
                'verbose_name': '오프라인 서비스',
                'verbose_name_plural': '오프라인 서비스',
                'db_table': 'offline_service',
            },
        ),
    ]
