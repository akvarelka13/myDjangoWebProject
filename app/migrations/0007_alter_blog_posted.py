# Generated by Django 4.1.7 on 2023-04-04 06:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_alter_blog_posted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='posted',
            field=models.DateTimeField(db_index=True, default=datetime.datetime(2023, 4, 4, 9, 44, 43, 148815), verbose_name='Опубликована'),
        ),
    ]
