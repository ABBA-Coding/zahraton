from aiogram.dispatcher import FSMContext

from keyboards.inline.menu_button import menu_keyboard
from loader import dp, bot
from aiogram import types

from utils.checker import process_subscription


@dp.message_handler(state=None)
async def bot_echo(message: types.Message, state: FSMContext):
    await message.answer("Bo'limni tanlang 👇", reply_markup=menu_keyboard())
    await state.set_state('user_menu')
    await state.update_data(action='menu')


@dp.callback_query_handler(lambda call: call.data == "approve", state="*")
async def command_start(callback: types.CallbackQuery, state):
    await callback.answer()
    if await process_subscription(callback.message, user_id=callback.from_user.id) is False:
        return
    await callback.message.answer("Bo'limni tanlang 👇", reply_markup=menu_keyboard())
    await callback.message.delete()
    await state.set_state('user_menu')
    await state.update_data(action='menu')
