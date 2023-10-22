import json
import os
import time

import requests
from celery import shared_task

from apps.main.models import Notification, NotificationShots
from apps.telegram_bot.models import TelegramChat

api_token = str(os.getenv("BOT_TOKEN"))
base_url = f'https://api.telegram.org/bot{api_token}'
SEND_MEDIA_GROUP = f"https://api.telegram.org/bot{api_token}/sendMediaGroup"


def send_media_group(text, chat_id, media):
    files = {}
    media_list = []
    for i, img_path in enumerate(media):
        with open(img_path, "rb") as img:
            files[f'photo{i}'] = img.read()
            media_list.append({'type': 'photo', 'media': f'attach://photo{i}'})
    media_list[0]['caption'] = text
    payload = {'chat_id': chat_id, 'media': json.dumps(media_list)}
    resp = requests.post(SEND_MEDIA_GROUP, data=payload, files=files)
    return resp.status_code


def send_notifications_text(text, chat_id, media=None):
    url = f'https://api.telegram.org/bot{api_token}/sendMessage'
    data = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, data=data)
    return response.status_code


@shared_task()
def send_notifications_task(notification_id, text, media):
    chats = TelegramChat.objects.filter(is_stopped=False)
    sended_count = 0
    send_notification_bound = send_media_group if media else send_notifications_text
    for i in chats:
        time.sleep(0.035)
        response = send_notification_bound(text=text,
                                           chat_id=i.telegram_id,
                                           media=media)
        if response == 200:
            sended_count += 1
        else:
            i.is_stopped = True
            i.save()
    notification = Notification.objects.get(id=notification_id)
    notification.all_chats = sended_count
    notification.status = notification.NotificationStatus.SENDED
    notification.save()
