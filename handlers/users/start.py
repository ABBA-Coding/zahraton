import random
from datetime import datetime

import phonenumbers

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardRemove

from loader import dp, bot
from keyboards.inline.menu_button import *
from keyboards.inline.main_inline import *
from utils.db_api.database import *


def check_date_convert(date_string):
    try:
        date_object = datetime.strptime(date_string, '%Y-%m-%d')
        formatted_year = str(date_object.year).zfill(2)
        formatted_month = str(date_object.month).zfill(2)
        formatted_day = str(date_object.day).zfill(2)
        if len(formatted_month) == len(formatted_day) == 2:
            return formatted_year, formatted_month, formatted_day
        return None, None, None
    except ValueError:
        return None, None, None


async def register_start_message(message: types.Message, state: FSMContext):
    await message.answer("👋 Assalomu alaykum\nZahratun botiga xush kelibsiz. Iltimos ism, sharifingizni kiriting",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state("get_name")


@dp.message_handler(commands=['register'], state='*')
async def register_func(message: types.Message, state: FSMContext, db: Database):
    await register_start_message(message, state)


@dp.message_handler(commands=['start'], state='*')
async def start_func(message: types.Message, state: FSMContext, db: Database):
    await db.add_chat(message.from_user.id)
    user = await db.get_user(message.from_user.id)
    if user and user['status'] is not False:
        keyboard = menu_keyboard()
        await message.answer("Zahratun supermarket botiga xush kelibsiz.\n\nBotda aksiyalar, yangiliklar, Zahratun "
                             "kartangiz balansi, foydali ma’lumotlar va izoh bildirish bo’limini topa olasiz. \n\n"
                             "Oilamizga marhamat 💚",
                             reply_markup=keyboard)
        await state.set_state("user_menu")
    else:
        await register_start_message(message, state)


@dp.message_handler(state='get_name')
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    keyboard = gender_keyboard()
    await message.answer('Iltimos jinsingizni kiriting 👇', reply_markup=keyboard)
    await state.set_state('get_gender')


@dp.message_handler(state='get_gender')
async def get_name(message: types.Message, state: FSMContext):
    gender = message.text[3:]
    if gender in [" Ayol", " Erkak"]:
        await state.update_data(gender=message.text[3:])
        await message.answer('Iltimos tug\'ilgan sanangizni <b>1980-12-24</b> shaklida kiriting kiriting 👇',
                             reply_markup=ReplyKeyboardRemove())
        await state.set_state('get_birth')
        return
    return await message.answer("Iltimos pasdagi tugmalardan birini tanlang 👇", reply_markup=gender_keyboard())


@dp.message_handler(state='get_birth')
async def get_name(message: types.Message, state: FSMContext):
    year, month, day = check_date_convert(message.text)
    if month is not None:
        await state.update_data(birth=str(year)+"-"+str(month)+"-"+str(day))
        # keyboard = await location_send()
        # await message.answer('Iltimos manzilingizni ulashing 👇', reply_markup=keyboard)
        # await state.set_state('get_location')
        await state.update_data(longitude=0, latitude=0)
        keyboard = phone_keyboard()
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
        keyboard = phone_keyboard()
        await message.answer("Telefon raqamingizni xalqaro formatda(998YYXXXXXXX) kiriting. Yoki raqamni ulashing 👇",
                             reply_markup=keyboard)
        await state.set_state('get_phone')
    else:
        keyboard = location_send()
        await message.answer('Iltimos manzilingizni kiriting 👇', reply_markup=keyboard)


@dp.message_handler(state='get_phone', content_types=types.ContentTypes.CONTACT)
async def get_phone(message: types.Message, state: FSMContext):
    phone_number = message.contact.phone_number
    parsed_number = phonenumbers.parse("+" + phone_number, None)
    is_valid = phonenumbers.is_valid_number(parsed_number)
    if is_valid:
        await state.update_data(phone=phone_number.replace("+", ""))
        await message.answer('Biz sizni malumotlaringizni qayta ishlashga ruhsat bering',
                             reply_markup=oferta_confirm())
        await state.set_state('confir_oferta')
    else:
        await message.answer("Telefon raqam noto'g'ri ko'rsatilgan")


@dp.message_handler(state='get_phone', content_types=types.ContentTypes.TEXT)
async def get_phone_text_validation(message: types.Message, state: FSMContext):
    await message.answer("Iltimos quyidagi tugmani bosib bizga telefon raqamingizni jo'nating 👇")


@dp.callback_query_handler(state='confir_oferta')
async def get_confirm(call: types.CallbackQuery, state: FSMContext, db: Database):
    call_data = call.data
    await call.answer()
    if call_data == 'confirm':
        data = await state.get_data()
        keyboard = menu_keyboard()
        await db.register_new_user(phone=data['phone'], gender=gender_mapper[data['gender']], name=data['name'],
                                   user_id=call.from_user.id, longitude=data['longitude'],
                                   latitude=data['latitude'], birth=data['birth'])
        await db.add_user(phone=data['phone'], name=data['name'],
                          telegram_id=call.from_user.id,
                          gender=gender_mapper[data['gender']], latitude=data['latitude'], longitude=data['longitude'],
                          birth=data['birth'])
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id,
                               text="👋 Bosh menyuga xush kelibsiz\nPastdagi tugmalar orqali kerakli buyruqni tanlang",
                               reply_markup=keyboard)
        await state.set_state("user_menu")
    elif call_data == 'cancel':
        await call.message.delete()
        await bot.send_message(chat_id=call.from_user.id, text="Botni ishga tushurish uchun /start tugmasini bosing",
                               reply_markup=ReplyKeyboardRemove())
