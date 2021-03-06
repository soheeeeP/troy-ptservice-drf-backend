# Generated by Django 3.2.5 on 2021-10-13 11:19

import datetime
import django.core.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20211008_0454'),
    ]

    operations = [
        migrations.AddField(
            model_name='bodyinfo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userprofile',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='bodyinfo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='birth',
            field=models.DateField(default=datetime.date(2020, 1, 1), validators=[django.core.validators.MinValueValidator(limit_value=datetime.date(1984, 1, 1)), django.core.validators.MaxValueValidator(limit_value=datetime.date(2021, 10, 12))], verbose_name='생년월일'),
        ),
    ]
