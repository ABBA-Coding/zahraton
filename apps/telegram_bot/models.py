from django.db import models
from datetime import datetime
from django.utils import timezone


class TelegramUser(models.Model):
    telegram_id = models.CharField(max_length=100, db_index=True)
    moneyback_id = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    full_name = models.CharField(max_length=1000, null=True, blank=True)
    password = models.CharField(max_length=100, null=True, blank=True)
    otp = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=1000, null=True, blank=True)
    longitude = models.CharField(max_length=1000, null=True, blank=True)
    latitude = models.CharField(max_length=1000, null=True, blank=True)
    birth = models.CharField(max_length=1000, null=True, blank=True)
    register_date = models.DateField(auto_now_add=True)

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
    register_date = models.DateField(auto_now_add=True)
    is_stopped = models.BooleanField(default=False)
