# Generated by Django 4.2 on 2023-07-16 05:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0003_telegramuser_latitude_telegramuser_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='birth',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]