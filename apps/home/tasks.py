import os
import requests
from celery import shared_task

from apps.main.models import Notification
from apps.telegram_bot.models import TelegramChat


api_token = str(os.getenv("BOT_TOKEN"))
base_url = f'https://api.telegram.org/bot{api_token}'


def send_notifications(text, chat_id, photo_url):
    url = f'{base_url}/sendPhoto'
    files = {'photo': open(f"/var/www/zahraton.itlink.uz/media/{photo_url}", 'rb')}
    data = {'chat_id': chat_id, 'caption': text}
    response = requests.post(url, files=files, data=data)
    return response.status_code

@shared_task()
def send_notifications_task(notification_id):
    # notification = Notification.objects.filter(pk=notification_id).first()
    # chats = TelegramChat.objects.all()
    # sended_count = 0
    # for i in chats:
    #     text = notification.description
    #     image_path = notification.ImageURL
    #     chat_id = i.telegram_id
    #     response = send_notifications(text=text, chat_id=chat_id, photo_url=image_path)
    #     if response == 200:
    #         sended_count += 1
    # notification.all_chats = sended_count
    # notification.status = notification.NotificationStatus.SENDED
    # notification.save()
    ...
