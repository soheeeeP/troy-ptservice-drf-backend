# Generated by Django 3.2.5 on 2021-08-31 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='trainee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.traineeprofile', verbose_name='트레이니'),
        ),
        migrations.AddField(
            model_name='service',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.trainerprofile', verbose_name='트레이너'),
        ),
        migrations.AddField(
            model_name='onlineservice',
            name='evaluation',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='services.evaluation', verbose_name='평가'),
        ),
        migrations.AddField(
            model_name='onlineservice',
            name='goal',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='services.goal'),
        ),
        migrations.AddField(
            model_name='onlineservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service', verbose_name='서비스'),
        ),
        migrations.AddField(
            model_name='offlineservice',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.service', verbose_name='서비스'),
        ),
    ]
