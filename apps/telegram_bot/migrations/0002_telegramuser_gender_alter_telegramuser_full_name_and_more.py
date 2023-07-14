# Generated by Django 4.2 on 2023-07-12 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('telegram_bot', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='telegramuser',
            name='gender',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='full_name',
            field=models.CharField(max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='moneyback_id',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='otp',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='telegramuser',
            name='phone',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
