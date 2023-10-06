from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.menu_button import *
from keyboards.inline.main_inline import *
from utils.db_api.database import *

import re
import aiohttp
import random

date_pattern = re.compile(r"\d{4}-\d{2}-\d{2}")


async def generateOTP():
    return random.randint(111111, 999999)


async def isValid(s):
    Pattern = re.compile("(0|91)?[7-9][0-9]{9}")
    return Pattern.match(s)


@dp.message_handler(commands=['start'], state='*')
async def start_func(message: types.Message, state: FSMContext):
    await add_chat(message.from_user.id)
    user = await get_user(message.from_user.id)
    if user is not None:
        keyboard = await menu_keyboard()
        await message.answer("Zahratun supermarket botiga xush kelibsiz.\n\nBotda aksiyalar, yangiliklar, Zahratun "
                             "kartangiz balansi, foydali ma’lumotlar va izoh bildirish bo’limini topa olasiz. \n\n"
                             "Oilamizga marhamat 💚",
                             reply_markup=keyboard)
        await state.set_state("user_menu")
    else:
        await message.answer("👋 Assalomu alaykum\nZahratun botiga xush kelibsiz. Iltimos ism, sharifingizni kiriting",
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
    await state.update_data(gender=message.text[3:])

    await message.answer('Iltimos tug\'ilgan sanangizni <b>1980-12-24</b> shaklida kiriting kiriting 👇',
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state('get_birth')


@dp.message_handler(state='get_birth')
async def get_name(message: types.Message, state: FSMContext):
    if date_pattern.match(message.text) is not None:
        await state.update_data(birth=message.text)
        # keyboard = await location_send()
        # await message.answer('Iltimos manzilingizni ulashing 👇', reply_markup=keyboard)
        # await state.set_state('get_location')
        await state.update_data(longitude=0, latitude=0)
        keyboard = await phone_keyboard()
        await message.answer("Telefon raqamingizni xalqaro formatda(998YYXXXXXXX) kiriting. Yoki raqamni ulashing 👇",
                             reply_markup=keyboard)
        await state.set_state('get_phone')
    else:
        await message.answer('Iltimos tug\'ilgan sanangizni <b>1980-12-24</b>(yil-oy-kun) shaklida kiriting kiriting 👇',
                             reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state='get_location', content_types=types.ContentTypes.LOCATION)
async def get_name(message: types.Message, state: FSMContext):
    if message.location:
        location = message.location
        Latitude = str(location.latitude)
        Longitude = str(location.longitude)
        await state.update_data(longitude=Longitude, latitude=Latitude)
        keyboard = await phone_keyboard()
        await message.answer("Telefon raqamingizni xalqaro formatda(998YYXXXXXXX) kiriting. Yoki raqamni ulashing 👇",
                             reply_markup=keyboard)
        await state.set_state('get_phone')
    else:
        keyboard = await location_send()
        await message.answer('Iltimos manzilingizni kiriting 👇', reply_markup=keyboard)


@dp.message_handler(state='get_phone', content_types=types.ContentTypes.CONTACT)
async def get_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    keyboard = await oferta_confirm()
    await state.update_data(phone=phone_number)
    await message.answer('Biz sizni malumotlaringizni qayta ishlashga ruhsat bering', reply_markup=keyboard)
    await state.set_state('confir_oferta')


@dp.message_handler(state='get_phone', content_types=types.ContentTypes.TEXT)
async def get_phone(message: types.Message, state: FSMContext):
    phone_number = message.text
    await state.update_data(phone=phone_number)
    keyboard = await oferta_confirm()
    await state.update_data(phone=phone_number)
    await message.answer('Biz sizni malumotlaringizni qayta ishlashga ruhsat bering', reply_markup=keyboard)
    await state.set_state('confir_oferta')


@dp.callback_query_handler(state='confir_oferta')
async def get_confirm(call: types.CallbackQuery, state: FSMContext):
    call_data = call.data
    if call_data == 'confirm':
        data = await state.get_data()
        keyboard = await menu_keyboard()
        user = await register_new_user(phone=data['phone'], gender=data['gender'], name=data['name'],
                                       user_id=call.from_user.id, longitude=data['longitude'],
                                       latitude=data['latitude'], birth=data['birth'])
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id,
                               text="👋 Bosh menyuga xush kelibsiz\nPastdagi tugmalar orqali kerakli buyruqni tanlang",
                               reply_markup=keyboard)
        await state.set_state("user_menu")
    elif call_data == 'cancel':
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text="Botni ishga tushurish uchun /start tugmasini bosing",
                               reply_markup=ReplyKeyboardRemove())

