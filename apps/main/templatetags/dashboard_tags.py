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
    )
    users_in_current_month = TelegramUser.objects.filter(
        Q(register_date__year=current_date.year) &
        Q(register_date__month=current_date.month)
    )

    telegram_chats = TelegramChat.objects.all()
    users = TelegramUser.objects.all()
    context = {
        'segment': 'dashboard',
        'telegram_chats': len(telegram_chats),
        'this_month_chats': len(chats_in_current_month),
        'this_month_users': len(users_in_current_month),
        'users': len(users),
        'cashbacks': []
    }

    return context
