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
def get_news(user_id):
    user = User.objects.filter(telegram_id=user_id).first()
    news = []
    for new in News.objects.all().order_by('-id'):
        if new.max_age == 0:
            new.max_age = 1000
            new.save()
        if new.check_user(age=user.age, gender=user.gender):
            news.append(new)
    return news


def add_user(phone, name, telegram_id, gender, latitude, longitude, birth, uuid=None):
    user, created = User.objects.get_or_create(
        phone=phone
    )
    user.telegram_id = telegram_id
    user.full_name = name
    user.gender = gender
    user.latitude = latitude
    user.longitude = longitude
    user.birth = birth
    user.save()
    return user


@sync_to_async
def register_new_user(gender, phone, name, user_id, longitude, latitude, birth):
    data = {
            "key": "e67ab364-bc13-11ec-8a51-0242ac12000d",
            "phone": phone,
            "firstName": name,
            "lastName": "NN",
            "gender": "1" if 'Ayol' in gender else "0",
            "birthDate": birth
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
        user = add_user(name=name, phone=phone, telegram_id=user_id, gender=gender, longitude=longitude,
                        latitude=latitude, birth=birth)
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
    keys = ['e67ab364-bc13-11ec-8a51-0242ac12000d', 'e67ab364-bc13-11ec-8a51-0242ac12000d',
            '340c3b26-59ac-11ed-91c5-0242ac12000f', 'b97c33b0-40e8-11ed-9ade-0242ac120008']
    url = f"https://cabinet.cashbek.uz/services/gocashapi/api/cheque-pageList?page={page}&size=3"
    orders = []
    for key in keys:
        data = {
            "key": key,
            "phone": phone
        }
        response = requests.post(url, json=data)
        orders += response.json()
    return orders
