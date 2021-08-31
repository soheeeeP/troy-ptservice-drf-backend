# Generated by Django 3.2.6 on 2021-08-26 10:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoalTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '목표 태그',
                'verbose_name_plural': '목표 태그',
                'db_table': 'goal_tag',
            },
        ),
        migrations.CreateModel(
            name='HashTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_type', models.CharField(choices=[('specialty', '전문성'), ('purpose', '목적'), ('goal', '목표')], max_length=20, verbose_name='태그 종류')),
                ('tag_content', models.CharField(max_length=20, verbose_name='태그 이름')),
            ],
            options={
                'verbose_name': '해시태그',
                'verbose_name_plural': '해시태그',
                'db_table': 'hash_tag',
            },
        ),
        migrations.CreateModel(
            name='PurposeTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': '목적 태그',
                'verbose_name_plural': '목적 태그',
                'db_table': 'purpose_tag',
            },
        ),
        migrations.CreateModel(
            name='SpecialtyTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tags.hashtag')),
            ],
            options={
                'verbose_name': '전문성 태그',
                'verbose_name_plural': '전문성 태그',
                'db_table': 'specialty_tag',
            },
        ),
    ]
