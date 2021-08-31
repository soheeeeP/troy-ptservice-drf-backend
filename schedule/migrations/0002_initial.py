# Generated by Django 3.2.6 on 2021-08-26 10:27

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
            model_name='trainerschedule',
            name='trainee',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.traineeprofile', verbose_name='트레이니'),
        ),
        migrations.AddField(
            model_name='trainerschedule',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.trainerprofile', verbose_name='트레이너'),
        ),
        migrations.AddField(
            model_name='reschedulerequest',
            name='trainee',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.traineeprofile', verbose_name='트레이니'),
        ),
        migrations.AddField(
            model_name='reschedulerequest',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.trainerprofile', verbose_name='트레이너'),
        ),
    ]
