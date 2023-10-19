from django.contrib import admin
from import_export.admin import ExportActionMixin
from django.db.models import Count
from .models import TelegramUser, TelegramChat


@admin.register(TelegramUser)
class TelegramUserAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ["serial_number", "telegram_id", "phone", "moneyback_id"]
    search_fields = ["phone"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(serial_number=Count('id'))
        return queryset

    def serial_number(self, obj):
        return obj.serial_number

    serial_number.short_description = '№'
    serial_number.admin_order_field = 'id'


@admin.register(TelegramChat)
class TelegramChatAdmin(admin.ModelAdmin):
    list_display = ["telegram_id", "register_date"]
