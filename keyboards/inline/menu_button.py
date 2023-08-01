from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.utils.callback_data import CallbackData
from apps.main.models import *


async def phone_keyboard():
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"📞 Raqamni ulashish", request_contact=True)
    key2 = KeyboardButton(text=f"⬅️ Orqaga")
    keyboard.add(key1)
    keyboard.resize_keyboard = True
    return keyboard


async def gender_keyboard():
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"👩‍💼 Ayol")
    key2 = KeyboardButton(text=f"👨‍💼 Erkak")
    keyboard.add(key1, key2)
    keyboard.resize_keyboard = True
    return keyboard


async def order_keyboard():
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f" Oldinga")
    key2 = KeyboardButton(text=f" Orqaga")
    key2 = KeyboardButton(text=f" Bosh menyuga")
    keyboard.add(key1, key2)
    keyboard.resize_keyboard = True
    return keyboard


async def back_key():
    keyboard = ReplyKeyboardMarkup()
    key1 = KeyboardButton(text=f"⬅️ Orqaga")
    keyboard.add(key1)
    keyboard.resize_keyboard = True
    return keyboard


async def menu_keyboard():
    keyboard = ReplyKeyboardMarkup(row_width=2)
    key1 = KeyboardButton(text=f"💰 Mening hisobim (bonuslarim)")
    key2 = KeyboardButton(text=f"🔄 QR kod")
    key3 = KeyboardButton(text=f"🎁 Aksiyalar")
    key4 = KeyboardButton(text=f"💳 To'lovlar tarixi")
    key5 = KeyboardButton(text=f"📰 Yangiliklar")
    key6 = KeyboardButton(text=f"📝 Taklif va shikoyatlar")
    keyboard.add(key1, key2, key3, key4, key5, key6)
    keyboard.resize_keyboard = True
    return keyboard


async def location_send():
    mrk = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    bt = KeyboardButton(f'📍 Joylashuvni ulashish', request_location=True)
    mrk.add(bt)
    return mrk

