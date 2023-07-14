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


async def send_sms(otp, phone):
    username = 'intouch'
    password = '-u62Yq-s79HR'
    sms_data = {
        "messages": [{"recipient": f"{phone}", "message-id": "abc000000003",
                      "sms": {"originator": "3700", "content": {"text": f"Ваш код подтверждения для BOT: {otp}"}}}]}
    url = "http://91.204.239.44/broker-api/send"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, auth=aiohttp.BasicAuth(login=username, password=password),
                                json=sms_data) as response:
            print(response.status)


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
        await message.answer("👋 Assalomu alaykum\nZahratoon botiga xush kelibsiz Iltimos ism, sharifingizni kiriting")
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
    await message.answer('Iltimos manzilingizni kiriting 👇', reply_markup=ReplyKeyboardRemove())
    await state.set_state('get_location')


@dp.message_handler(state='get_location')
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(location=message.text)
    keyboard = await phone_keyboard()
    await message.answer("Telefon raqamininfizni xalqaro formatda(998YYXXXXXXX) kiriting. Yoki raqamni ulashing 👇",
                         reply_markup=keyboard)
    await state.set_state('get_phone')


@dp.message_handler(state='get_phone', content_types=types.ContentTypes.CONTACT)
async def get_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number.split('+')[1]
    keyboard = await back_key()
    await state.update_data(phone=phone_number)
    data = await state.get_data()
    await message.answer(f"{phone_number} raqamiga yuborilgan 📩 SMS ni kiriting 👇", reply_markup=keyboard)
    await state.set_state('get_otp')


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
        await message.answer(f"{phone_number} raqamiga yozilgan 📩 SMS ni kiriting 👇", reply_markup=back_keyboard)
        await state.set_state("get_otp")


@dp.message_handler(state='get_otp', content_types=types.ContentTypes.TEXT)
async def get_phone(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.text == '11':
        keyboard = await menu_keyboard()
        user = await register_new_user(phone=data['phone'], gender=data['gender'], name=data['name'],
                                user_id=message.from_user.id)
        await message.answer("👋 Bosh menu ga xush kelibsiz\nPastdagi tugmalar orqali kerakli buyruqni tanlang", reply_markup=keyboard)
        await state.set_state("user_menu")
    else:
        await message.answer("❌ Kiritiltgan tasdiqlash kodi xato. Qayta unirib ko'ring")
