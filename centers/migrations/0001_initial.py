# Generated by Django 3.2.5 on 2021-08-09 06:32

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Center',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', django.contrib.gis.db.models.fields.PointField(db_index=True, srid=4326, verbose_name='위치')),
                ('name', models.CharField(max_length=50, verbose_name='장소명')),
                ('full_address', models.CharField(max_length=100, verbose_name='주소')),
                ('city', models.CharField(max_length=50, null=True, verbose_name='시/도')),
                ('district', models.CharField(max_length=50, null=True, verbose_name='시/군/구')),
                ('town', models.CharField(max_length=50, null=True, verbose_name='읍/면/동')),
            ],
            options={
                'verbose_name': '센터',
                'verbose_name_plural': '센터',
                'db_table': 'center',
            },
        ),
    ]
