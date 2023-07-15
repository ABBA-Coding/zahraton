from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.menu_button import *
from utils.db_api.database import *

import re
import aiohttp
import random


async def generateOTP():
    return random.randint(111111, 999999)


async def isValid(s):
    Pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    return Pattern.match(s)


@dp.message_handler(commands=['start'], state='*')
async def start_func(message: types.Message, state: FSMContext):
    user = await get_user(message.from_user.id)
    if user is not None:
        keyboard = await menu_keyboard()
        await message.answer("Bosh menyuga xush kelibsiz. Kerakli tugmani tanlang.", reply_markup=keyboard)
        await state.set_state("user_menu")
    else:
        await message.answer("👋 Assalomu alaykum\nZahratoon botiga xush kelibsiz Iltimos ism, sharifingizni kiriting",
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state("get_name")


@dp.message_handler(state='get_name')
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    keyboard = await gender_keyboard()
    await message.answer('Iltimos jinsingizni kiriting 👇', reply_markup=keyboard)
    await state.set_state('get_gender')


@dp.message_handler(state='get_gender')
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(gender=message.text[1:])
    keyboard = await location_send()
    await message.answer('Iltimos manzilingizni kiriting 👇', reply_markup=keyboard)
    await state.set_state('get_location')


@dp.message_handler(state='get_location', content_types=types.ContentTypes.LOCATION)
async def get_name(message: types.Message, state: FSMContext):
    if message.location:
        location = message.location
        Latitude = str(location.latitude)
        Longitude = str(location.longitude)
        await state.update_data(longitude=Longitude, latitude=Latitude)
        keyboard = await phone_keyboard()
        await message.answer("Telefon raqamininfizni xalqaro formatda(998YYXXXXXXX) kiriting. Yoki raqamni ulashing 👇",
                             reply_markup=keyboard)
        await state.set_state('get_phone')
    else:
        keyboard = await location_send()
        await message.answer('Iltimos manzilingizni kiriting 👇', reply_markup=keyboard)


@dp.message_handler(state='get_phone', content_types=types.ContentTypes.CONTACT)
async def get_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    keyboard = await back_key()
    data = await state.get_data()
    await state.update_data(phone=phone_number)
    keyboard = await menu_keyboard()
    user = await register_new_user(phone=phone_number, gender=data['gender'], name=data['name'],
                                   user_id=message.from_user.id, longitude=data['longitude'],
                                   latitude=data['latitude'])
    await message.answer("👋 Bosh menu ga xush kelibsiz\nPastdagi tugmalar orqali kerakli buyruqni tanlang",
                         reply_markup=keyboard)
    await state.set_state("user_menu")


@dp.message_handler(state='get_phone', content_types=types.ContentTypes.TEXT)
async def get_phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    if not await isValid(phone_number):
        keyboard = await phone_keyboard()
        await message.answer("⚠️ Telefon raqamingizni noto'g'ri kiritdingiz. Iltimos, qaytadan kiriting.",
                             reply_markup=keyboard)
        return
    else:
        await state.update_data(phone=phone_number)
        back_keyboard = await back_key()
        data = await state.get_data()
        keyboard = await menu_keyboard()
        user = await register_new_user(phone=phone_number, gender=data['gender'], name=data['name'],
                                       user_id=message.from_user.id, longitude=data['longitude'],
                                       latitude=data['latitude'])
        await message.answer("👋 Bosh menu ga xush kelibsiz\nPastdagi tugmalar orqali kerakli buyruqni tanlang",
                             reply_markup=keyboard)
        await state.set_state("user_menu")


#
# @dp.message_handler(state='get_otp', content_types=types.ContentTypes.TEXT)
# async def get_phone(message: types.Message, state: FSMContext):
#     data = await state.get_data()
#     if message.text == '11':
#     else:
#         await message.answer("❌ Kiritiltgan tasdiqlash kodi xato. Qayta unirib ko'ring")
