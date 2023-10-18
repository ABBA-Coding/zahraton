from keyboards.inline.menu_button import menu_keyboard
from loader import dp, bot
from aiogram import types


@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    await message.answer("Bo'limni tanlang 👇", reply_markup=menu_keyboard())
