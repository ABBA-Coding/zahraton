from django.db import models
from apps.authentication.models import MegaUser as User
from apps.home.models import BaseModel
from ckeditor.fields import RichTextField
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
    name = models.CharField(verbose_name="Nomi", max_length=70, null=True, blank=True)
    description = RichTextField(verbose_name="Izoh", max_length=950)

    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Aksiya "
        verbose_name_plural = "Aksiyalar "

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


class SaleShots(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Rasm", upload_to="sales")

    class Meta:
        verbose_name = "Aksiya rasmi"
        verbose_name_plural = "Aksiya rasmlari"


class News(BaseModel):
    GENDER = (
        (ERKAK, ERKAK),
        (AYOL, AYOL),
        (ALL, ALL)
    )

    name = models.CharField(max_length=100, null=True, blank=True)
    description = RichTextField(max_length=940, null=True, blank=True)
    min_age = models.IntegerField(verbose_name="Qaysi yoshdan", default=0)
    max_age = models.IntegerField(verbose_name="Qaysi yoshgacha", default=100)
    for_gender = models.CharField(verbose_name="Kimlar uchun", max_length=200, choices=GENDER, null=True)

    active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Yangilik "
        verbose_name_plural = "Yangiliklar "


class NewsShots(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Rasm", upload_to="news")

    class Meta:
        verbose_name = "Yangilik rasmi "
        verbose_name_plural = "Yangilik rasmlari "


class Comment(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=4500)


class Notification(models.Model):
    class NotificationStatus(models.IntegerChoices):
        CREATED = 0, "Yaratildi"
        SENDED = 1, "Bitirildi"

    description = RichTextField(max_length=1023, null=True, blank=True)
    status = models.IntegerField(choices=NotificationStatus.choices, default=NotificationStatus.CREATED, editable=False)
    all_chats = models.IntegerField(default=0, editable=False)

    class Meta:
        verbose_name = "Bildirishnoma "
        verbose_name_plural = "Bildirishnomalar "


class NotificationShots(models.Model):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    image = models.ImageField(verbose_name="Rasm", upload_to="notification")

    class Meta:
        verbose_name = "Bildirishnoma rasmi "
        verbose_name_plural = "Bildirishnoma rasmlari "
