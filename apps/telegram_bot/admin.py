from django.contrib import admin
from .models import TelegramUser, TelegramChat


admin.site.register(TelegramUser)
admin.site.register(TelegramChat)
# Register your models here.
