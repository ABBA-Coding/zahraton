from django.contrib import admin
from import_export.admin import ExportActionMixin

from .models import TelegramUser, TelegramChat


@admin.register(TelegramUser)
class TelegramUserAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["telegram_id", "phone", "moneyback_id"]
    search_fields = ["phone"]


@admin.register(TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ["telegram_id", "register_date"]
