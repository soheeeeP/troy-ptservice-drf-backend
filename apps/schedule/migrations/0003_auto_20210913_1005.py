# Generated by Django 3.2.5 on 2021-09-13 10:05

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
        ('schedule', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('schedule_status', models.CharField(choices=[('opened', '수업개설'), ('scheduled', '예약완료')], default='opened', max_length=30, verbose_name='예약 상태')),
                ('date', models.DateField(verbose_name='수업일자')),
                ('time', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)], verbose_name='수업시간(30분_단위)')),
                ('coach', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.coachprofile', verbose_name='코치')),
                ('trainee', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.traineeprofile', verbose_name='트레이니')),
            ],
        ),
        migrations.RenameField(
            model_name='reschedulerequest',
            old_name='fixed_date',
            new_name='fixed_datetime',
        ),
        migrations.RenameField(
            model_name='reschedulerequest',
            old_name='requested_datetime',
            new_name='pub_datetime',
        ),
        migrations.RemoveField(
            model_name='reschedulerequest',
            name='approval',
        ),
        migrations.AddField(
            model_name='reschedulerequest',
            name='origin_end_time',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)]),
        ),
        migrations.AddField(
            model_name='reschedulerequest',
            name='origin_start_time',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)]),
        ),
        migrations.AddField(
            model_name='reschedulerequest',
            name='reschedule',
            field=models.CharField(choices=[('reschedule_request', '수업변경 요청'), ('reschedule_approval', '변경요청 승인'), ('reschedule_refusal', '변경요청 거부')], default='reschedule_request', max_length=30, verbose_name='변경 상태'),
        ),
        migrations.AddField(
            model_name='reschedulerequest',
            name='update_end_time',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)]),
        ),
        migrations.AddField(
            model_name='reschedulerequest',
            name='update_start_time',
            field=models.PositiveSmallIntegerField(default=0, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)]),
        ),
        migrations.DeleteModel(
            name='CoachSchedule',
        ),
    ]
