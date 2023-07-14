from django.db import models
from apps.authentication.models import MegaUser as User
from apps.home.models import BaseModel
from datetime import datetime, timedelta
from apps.telegram_bot.models import TelegramUser

MONTH, SEASON, YEAR = (
    "month",
    "season",
    "year"
)


class Sale(BaseModel):
    name = models.CharField(max_length=10000, null=True, blank=True)
    description = models.CharField(max_length=10000, null=True, blank=True)
    image = models.ImageField(null=True)
    
    active = models.BooleanField(default=True)

    @property
    def PhotoURL(self):
        try:
            return self.image.url
        except:
            return ''


class News(BaseModel):
    name = models.CharField(max_length=10000, null=True, blank=True)
    description = models.CharField(max_length=10000, null=True, blank=True)
    image = models.ImageField(null=True)

    active = models.BooleanField(default=True)

    @property
    def PhotoURL(self):
        try:
            return self.image.url
        except:
            return ''


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=4500)    

