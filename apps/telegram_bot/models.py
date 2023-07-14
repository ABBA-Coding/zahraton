from django.db import models


class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=100)
    moneyback_id = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=1000, null=True)
    password = models.CharField(max_length=100, null=True)
    otp = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
