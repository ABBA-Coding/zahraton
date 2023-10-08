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
            decoded_url = unquote(self.image.name)
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
    image = models.ImageField(null=True, blank=True)
    image2 = models.ImageField(null=True, blank=True)
    image3 = models.ImageField(null=True, blank=True)
    image4 = models.ImageField(null=True, blank=True)
    image5 = models.ImageField(null=True, blank=True)
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
            decoded_url = unquote(self.image.name)
            return decoded_url
        except:
            return ''

    @property
    def Photo2URL(self):
        try:
            return self.image2.url
        except:
            return ''

    @property
    def Image2URL(self):
        try:
            decoded_url = unquote(self.image2.name)
            return decoded_url
        except:
            return ''

    @property
    def Photo3URL(self):
        try:
            return self.image3.url
        except:
            return ''

    @property
    def Image3URL(self):
        try:
            decoded_url = unquote(self.image3.name)
            return decoded_url
        except:
            return ''

    @property
    def Photo4URL(self):
        try:
            return self.image4.url
        except:
            return ''

    @property
    def Image4URL(self):
        try:
            decoded_url = unquote(self.image4.name)
            return decoded_url
        except:
            return ''

    @property
    def Photo5URL(self):
        try:
            return self.image5.url
        except:
            return ''

    @property
    def Image5URL(self):
        try:
            decoded_url = unquote(self.image5.name)
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


class Notification(models.Model):
    description = models.CharField(max_length=10000, null=True, blank=True)
    image = models.ImageField(null=True)

    all_chats = models.IntegerField(default=0)

    @property
    def ImageURL(self):
        try:
            decoded_url = unquote(self.image.name)
            return decoded_url
        except:
            return ''

    @property
    def PhotoURL(self):
        try:
            return self.image.url
        except:
            return ''
