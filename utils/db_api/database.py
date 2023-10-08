from asgiref.sync import sync_to_async
from apps.telegram_bot.models import TelegramUser as User, TelegramChat
from apps.main.models import Sale, Comment, News
import requests
import json


@sync_to_async
def get_user(user_id):
    try:
        url = f'http://127.0.0.1:8000/api/get_user?user_id={user_id}'

        response = requests.get(url)
        data = response.status_code
        print(data)
        return response.json()
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
def add_chat(chat_id):
    chat, created = TelegramChat.objects.get_or_create(telegram_id=chat_id)
    chat.save()


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
    data = {
        'phone': phone,
        'telegram_id': telegram_id,
        'full_name': name,
        'gender': gender,
        'latitude': latitude,
        'longitude': longitude,
        'birth': birth,
    }
    url = 'http://127.0.0.1:8000/api/post_user/'

    response = requests.post(url, data=data)

    # Check the response status code to see if the request was successful
    if response.status_code == 201:  # 201 Created status code for a successful POST request
        print('User created successfully')
    else:
        print('Failed to create user')
        print(response.status_code)
        print(response.text)

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
    print(phone)
    user_uuid = get_api_uuid(phone)
    print(user_uuid)
    url = "https://cabinet.cashbek.uz/services/gocashapi/api/get-user-balance"
    data = {
        "key": "e67ab364-bc13-11ec-8a51-0242ac12000d",
        "clientCode": int(user_uuid)
    }

    response = requests.post(url, json=data)
    return response.json()


@sync_to_async
def get_user_orders(phone, page=None):
    keys = ['e67ab364-bc13-11ec-8a51-0242ac12000d', 'e67ab364-bc13-11ec-8a51-0242ac12000d',
            '340c3b26-59ac-11ed-91c5-0242ac12000f', 'b97c33b0-40e8-11ed-9ade-0242ac120008']
    url = f"https://cabinet.cashbek.uz/services/gocashapi/api/cheque-pageList"
    orders = []
    for key in keys:
        data = {
            "key": key,
            "phone": phone
        }
        response = requests.post(url, json=data)
        orders += response.json()
        filename = f'./jsons/{phone}.json'
        with open(filename, 'w') as file:
            json.dump(orders, file)
    return orders


@sync_to_async
def get_order_years(phone):
    with open(f'./jsons/{phone}.json') as file:
        data = json.load(file)

    years = set()
    for obj in data:
        cheque_date = obj['chequeDate']
        year = cheque_date[:4]
        years.add(year)
    return list(years)


@sync_to_async
def get_order_month(phone, year):
    with open(f'./jsons/{phone}.json') as file:
        data = json.load(file)

    months = set()
    for obj in data:
        cheque_date = obj['chequeDate']
        order_year = cheque_date[:4]
        if order_year == year:
            month = cheque_date[5:7]
            months.add(month)
    return list(months)


@sync_to_async
def get_orders_by_month(phone, year, month):
    with open(f'./jsons/{phone}.json') as file:
        data = json.load(file)
    orders = []
    for obj in data:
        cheque_date = obj['chequeDate']
        order_year = cheque_date[:4]
        order_month = cheque_date[5:7]
        if year == order_year and month == order_month:
            orders.append(obj)
    return orders

