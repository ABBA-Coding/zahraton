# Generated by Django 4.2 on 2023-10-08 03:54

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0007_alter_telegramchat_register_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='telegramuser',
            name='register_date',
            field=models.DateField(blank=True, default=datetime.date(2023, 10, 8), null=True),
        ),
    ]