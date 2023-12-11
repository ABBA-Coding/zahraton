from django import template
from apps.telegram_bot.models import *
from datetime import datetime
from django.db.models import Q

register = template.Library()


@register.inclusion_tag('admin/dashboard_stats.html')
def get_dashboard_stats():
    current_date = datetime.now()
    chats_in_current_month = TelegramChat.objects.filter(
        Q(register_date__year=current_date.year) &
        Q(register_date__month=current_date.month)
    ).count()
    users_in_current_month = TelegramUser.objects.filter(
        Q(register_date__year=current_date.year) &
        Q(register_date__month=current_date.month)
    ).count()

    telegram_chats_count = TelegramChat.objects.filter(is_stopped=False).count()
    blocked_chats_count = TelegramChat.objects.filter(is_stopped=True).count()
    users = TelegramUser.objects.all().count()
    context = {
        'segment': 'dashboard',
        'telegram_chats': telegram_chats_count,
        'this_month_chats': chats_in_current_month,
        'this_month_users': users_in_current_month,
        'users': users,
        "blocked_chats": blocked_chats_count,
        'cashbacks': []
    }

    return context
