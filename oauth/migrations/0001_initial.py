# Generated by Django 3.2.5 on 2021-09-10 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oauth_type', models.CharField(choices=[('Google', 'google'), ('default', 'default')], default='default', max_length=10, verbose_name='OAuth_Type')),
                ('oauth_token', models.CharField(db_index=True, default='', max_length=255, verbose_name='OAuth_ID')),
            ],
        ),
    ]
