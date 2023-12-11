import json
import os
import time

import requests
from celery import shared_task
from celery.utils.log import get_task_logger
from django.db.models import F

from apps.main.models import Notification
from apps.telegram_bot.models import TelegramChat

api_token = str(os.getenv("BOT_TOKEN"))
base_url = f'https://api.telegram.org/bot{api_token}'
SEND_MEDIA_GROUP = f"https://api.telegram.org/bot{api_token}/sendMediaGroup"

logger = get_task_logger(__name__)

CHUNK_SIZE = 4000


def send_media_group(text, chat_id, media):
    files = {}
    media_list = []
    for i, img_path in enumerate(media):
        with open(img_path, "rb") as img:
            files[f'photo{i}'] = img.read()
            media_list.append({'type': 'photo', 'media': f'attach://photo{i}'})
    media_list[0]['caption'] = text
    media_list[0]['parse_mode'] = 'HTML'

    payload = {'chat_id': chat_id, 'media': json.dumps(media_list)}
    resp = requests.post(SEND_MEDIA_GROUP, data=payload, files=files)
    return resp.status_code


def send_notifications_text(text, chat_id, media=None):
    url = f'https://api.telegram.org/bot{api_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': text, 'parse_mode': 'HTML'}
    response = requests.post(url, data=data)
    return response.status_code


@shared_task()
def send_notifications_task(notification_id, text, media, offset, chunk_size):
    chunk_chats = TelegramChat.objects.filter(is_stopped=False).order_by('id')[offset:offset + chunk_size]

    for chat in chunk_chats:
        send_notification_bound = send_media_group if media else send_notifications_text
        response = send_notification_bound(text=text, chat_id=chat.telegram_id, media=media)
        time.sleep(0.035)
        if response == 200:
            chat.is_stopped = False  # Reset is_stopped flag if the message was sent successfully
            chat.save()
        else:
            chat.is_stopped = True
            chat.save()

    Notification.objects.filter(id=notification_id).update(
        all_chats=F('all_chats') + chunk_chats.count(),
        status=Notification.NotificationStatus.SENDED
    )
