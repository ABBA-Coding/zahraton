from django.db import models
from apps.authentication.models import MegaUser as User
from apps.home.models import BaseModel
from datetime import datetime, timedelta
from apps.telegram_bot.models import TelegramUser
from urllib.parse import unquote


MONTH, SEASON, YEAR = (
    "month",
    "season",
    "year"
)


ERKAK, AYOL, ALL = (
    "👨‍💼 Erkaklar uchun",
    "👩‍💼 Ayollar uchun",
    "Hamma uchun"
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

    @property
    def ImageURL(self):
        try:
            decoded_url = unquote(self.image.url)
            return decoded_url
        except:
            return ''


class News(BaseModel):
    GENDER = (
        (ERKAK, ERKAK),
        (AYOL, AYOL),
        (ALL, ALL)
    )

    name = models.CharField(max_length=10000, null=True, blank=True)
    description = models.CharField(max_length=10000, null=True, blank=True)
    image = models.ImageField(null=True)
    min_age = models.IntegerField(default=0)
    max_age = models.IntegerField(default=100)
    for_gender = models.CharField(max_length=200, choices=GENDER, null=True)

    active = models.BooleanField(default=True)

    @property
    def PhotoURL(self):
        try:
            return self.image.url
        except:
            return ''

    @property
    def ImageURL(self):
        try:
            decoded_url = unquote(self.image.url)
            return decoded_url
        except:
            return ''

    def check_user(self, age, gender):
        if self.for_gender == "Hamma uchun" or gender in self.for_gender:
            if self.min_age <= age <= self.max_age:
                return True
        return False


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=4500)    

