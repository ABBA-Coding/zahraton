from django.db import models
from datetime import datetime


class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=100)
    moneyback_id = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    full_name = models.CharField(max_length=1000, null=True)
    password = models.CharField(max_length=100, null=True)
    otp = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=1000, null=True)
    longitude = models.CharField(max_length=1000, null=True)
    latitude = models.CharField(max_length=1000, null=True)
    birth = models.CharField(max_length=1000, null=True)

    @property
    def age(self):
        current_date = datetime.now()
        birth_date = datetime.strptime(self.birth, '%Y-%m-%d')
        age = current_date.year - birth_date.year

        if current_date.month < birth_date.month or (
                current_date.month == birth_date.month and current_date.day < birth_date.day):
            age -= 1

        return age


class TelegramChat(models.Model):
    telegram_id = models.CharField(max_length=100)
