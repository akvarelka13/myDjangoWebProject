# Generated by Django 4.1.7 on 2023-04-03 10:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 4, 3, 13, 37, 51, 194582), verbose_name='Опубликована'),
        ),
    ]
