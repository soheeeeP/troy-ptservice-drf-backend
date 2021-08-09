# Generated by Django 3.2.5 on 2021-08-05 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tags', '0003_alter_hashtag_tag_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hashtag',
            name='tag_type',
            field=models.CharField(choices=[('goal', '목표'), ('specialty', '전문성'), ('purpose', '목적')], default='goal', max_length=20, verbose_name='태그 종류'),
        ),
    ]