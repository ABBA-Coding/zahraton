from asgiref.sync import sync_to_async
from apps.telegram_bot.models import TelegramUser as User
from apps.main.models import Sale, Comment, News
import requests


@sync_to_async
def get_user(user_id):
    try:
        user = User.objects.get(telegram_id=user_id)
        return user
    except:    
        return None 

    
@sync_to_async
def get_user_by_phone(phone):
    try:
        user = User.objects.filter(phone=phone).first()
        return user
    except:
        return None


@sync_to_async
def set_user_telegram(user_id, phone, name):
    try:
        user = User.objects.get(phone=phone)
        user.telegram_id = user_id
        user.name = name
        user.save()
        return user
    except:
        return None


@sync_to_async
def get_active_sales_all():
    try:
        sale = Sale.objects.all().order_by('-id')
        return sale
    except:
        return None


@sync_to_async 
def add_comment(user_id, comment):
    pass
    # user = User.objects.get(telegram_id=user_id)
    # return Comment(user=user, comment=comment)


@sync_to_async
def get_news():
    return News.object.filter().all()


def add_user(phone, name, telegram_id, gender, uuid=None):
    user, created = User.objects.get_or_create(
        phone=phone
    )
    user.telegram_id = telegram_id
    user.full_name = name
    user.gender = gender
    user.save()
    return user


@sync_to_async
def register_new_user(gender, phone, name, user_id, location):
    data = {
            "key": "e67ab364-bc13-11ec-8a51-0242ac12000d",
            "phone": phone,
            "firstName": name,
            "lastName": "NN",
            "gender": "1" if 'Ayol' in gender else "0",
            "birthDate": "1980-01-01"
    }
    url = "https://cabinet.cashbek.uz/services/gocashapi/api/register-client"
    requests.post(url, json=data)

    url = "https://cabinet.cashbek.uz/services/gocashapi/api/get-uuid"
    payload = {
        "key": "e67ab364-bc13-11ec-8a51-0242ac12000d",
        "phone": phone
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200 and 'userUUID' in response.json():
        user = add_user(name=name, phone=phone, telegram_id=user_id, gender=gender)
        return user
    else:
        return None


def get_api_uuid(phone):
    url = "https://cabinet.cashbek.uz/services/gocashapi/api/get-uuid"
    payload = {
        "key": "e67ab364-bc13-11ec-8a51-0242ac12000d",
        "phone": phone
    }

    response = requests.post(url, json=payload)
    if response.status_code == 200 and 'userUUID' in response.json():
        return response.json()['userUUID']


@sync_to_async
def get_user_balance(phone):
    user_uuid = get_api_uuid(phone)
    url = "https://cabinet.cashbek.uz/services/gocashapi/api/get-user-balance"
    data = {
        "key": "e67ab364-bc13-11ec-8a51-0242ac12000d",
        "clientCode": int(user_uuid)
    }

    response = requests.post(url, json=data)
    return response.json()


@sync_to_async
def get_user_orders(phone, page):
    url = f"https://cabinet.cashbek.uz/services/gocashapi/api/cheque-pageList?page={page}&size=5"
    data = {
        "key": "e67ab364-bc13-11ec-8a51-0242ac12000d",
        "phone": phone
    }
    response = requests.post(url, json=data)
    return response.json()