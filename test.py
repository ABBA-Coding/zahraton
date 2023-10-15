import phonenumbers
from apps.telegram_bot.models import TelegramUser
users = TelegramUser.objects.all()
counter = 0
for user in users:
    try:
        c = phonenumbers.parse("+" + user.phone, None)
        is_valid = phonenumbers.is_valid_number(c)
        if not is_valid:
            counter += 1
            print(user.phone)
    except:
        counter += 1
        print(user.phone)


for user in users:
    user.phone = user.phone.replace(" ", "")
    user.save()

for user in users:
    if user.phone.startswith("98") and len(user.phone) == 11:
        user.phone = "9" + user.phone
        user.save()

counter = 0
for user in users:
    if len(user.phone) > 12:
        print(user.phone)
        counter += 1

for user in users:
    if user.phone.startswith("("):
        user.phone = user.phone[1:]
        user.save()


counter = 0
for user in users:
    if len(user.phone) == 9:
        user.phone = "998" + user.phone