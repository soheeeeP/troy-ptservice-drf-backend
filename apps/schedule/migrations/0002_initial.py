# Generated by Django 3.2.5 on 2021-09-10 11:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reschedulerequest',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.coachprofile', verbose_name='코치'),
        ),
        migrations.AddField(
            model_name='reschedulerequest',
            name='trainee',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.traineeprofile', verbose_name='트레이니'),
        ),
        migrations.AddField(
            model_name='coachschedule',
            name='coach',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.coachprofile', verbose_name='코치'),
        ),
        migrations.AddField(
            model_name='coachschedule',
            name='trainee',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.traineeprofile', verbose_name='트레이니'),
        ),
    ]
