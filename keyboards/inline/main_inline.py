from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from utils.db_api.database import *


async def move_keyboard():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"⬅️ Oldingi", callback_data="back"),
             InlineKeyboardButton(text=f"Keyingi ➡️", callback_data="next")],
        ]
    )
    return markup


async def sale_confirm(sale_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"✅ Qo'shilish", callback_data=f"{sale_id}")],
            [InlineKeyboardButton(text=f"⬅️ Ortga", callback_data="back")],
        ]
    )
    return markup


async def oferta_confirm():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=f"Sodiqlik dasturi qoidalari",
                                  url=f"https://docs.google.com/document/d"
                                      f"/1GrgAg41OZ_w8FAv6SOCEa7FMknGOPFiBTF_75QpD6zQ/edit?usp=sharing")],
            [
                InlineKeyboardButton(text=f"✅ Roziman", callback_data=f"confirm"),
                InlineKeyboardButton(text=f"❌ Rad etish", callback_data="cancel")
            ],
        ]
    )
    return markup


def year_keyboard(years):
    inline_keyboard = []
    for i in years:
        inline_keyboard.append([InlineKeyboardButton(text=f"{i}", callback_data=i)])
    inline_keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data=f"back_menu")])
    markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return markup


Moths = {'01': 'Yanvar', '02': 'Fevral', '03': 'Mart', '04': 'Aprel', '05': 'May', '06': 'Iyun', '07': 'Iyul',
         '08': 'Avgust', '09': 'Sentabr', '10': 'Oktyabr', '11': 'Noyabr', '12': 'Dekabr', }


async def month_keyboard(date):
    inline_keyboard = []
    row = []
    count = 0
    for i in date:
        row.append(InlineKeyboardButton(text=f"{Moths[i]}", callback_data=i))
        count += 1
        if count == 3:
            inline_keyboard.append(row)
            row = []
            count = 0
    if row:
        inline_keyboard.append(row)
        inline_keyboard.append([InlineKeyboardButton(text="🔙 Orqaga", callback_data="back_menu")])
        markup = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
        return markup
