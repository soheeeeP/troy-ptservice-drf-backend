# Generated by Django 3.2.6 on 2021-08-26 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('services', '0002_initial'),
        ('tags', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialtytag',
            name='trainer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.trainerprofile'),
        ),
        migrations.AddField(
            model_name='purposetag',
            name='tag_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.hashtag'),
        ),
        migrations.AddField(
            model_name='purposetag',
            name='trainee_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.traineeprofile'),
        ),
        migrations.AddField(
            model_name='goaltag',
            name='goal_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='services.goal'),
        ),
        migrations.AddField(
            model_name='goaltag',
            name='tag_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.hashtag'),
        ),
    ]
