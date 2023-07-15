from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.menu_button import *
from keyboards.inline.main_inline import *
from utils.db_api.database import *
import qrcode


@dp.message_handler(state='user_menu')
async def menu(message: types.Message, state: FSMContext):
    await state.update_data(action='menu')
    user = await get_user(user_id=message.from_user.id)
    if message.text == "Mening hisobim/Bonuslarim":
        keyboard = await menu_keyboard()
        orders_m = 0
        cashbacks = 0
        text = f"\n\nHozirgi keshbek: {cashbacks}"
        await message.answer(text, reply_markup=keyboard)
    if message.text == "Joriy aksiyalar":
        await state.update_data(sale_id=0)
        back_keyboard = await back_key()
        await message.answer("Hozirda aktiv bo'lgan aksiyalar 👇", reply_markup=back_keyboard)
        sale = await get_active_sales_all()
        sale = sale[0]
        text = f"🔥 {sale.name}\n\n 🎁{sale.description} "
        keyboard = await move_keyboard()
        await message.answer(text, reply_markup=keyboard)
        await state.set_state('aksiya')
    if message.text == "Izoh qoldirish":
        keyboard = await back_key()
        await message.answer("ltimos o'z izohingizni shu yerda yozib qoldiring 👇\n"
                             "Mutaxassislarimiz o'rganib chiqib tez orada sizga "
                             "javob berishadi", 
                             reply_markup=keyboard)
        await state.set_state("get_comment")
    if message.text == 'QrCode':
        balance = await get_user_balance(user.phone)
        user_uuid = get_api_uuid(user.phone)
        q = qrcode.make(f'{user_uuid}')
        q.save('qrcode.png')
        keyboard = await menu_keyboard()
        photo = open('qrcode.png', 'rb')
        await message.answer_photo(photo=photo, caption=f"Sizning keshbekingizni ishlatish uchun QR codingiz "
                                                        f"👆\n\nHozirgi keshbekingiz: {balance['balance']} UZS",
                                   reply_markup=keyboard)
    if message.text == "To'lovlar tarixi":
        orders = await get_user_orders(phone=message.from_user.id, page=0)
        page = 0
        text = "To'lovlar tarixi bo'limi\n"
        back_keyboard = await back_key()
        await message.answer(text, reply_markup=back_keyboard)
        if orders:
            text = ''
            i = 1
            for order in orders:
                datetime_obj = datetime.strptime(order['chequeDate'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                formatted_datetime = datetime_obj.strftime("%d.%m.%Y %H:%M")
                text += f"\n\n{i}) 📆 Sana: {formatted_datetime}\n    💲 Jami: {order['totalAmount']}"
                for order_detail in order['products']:
                    text += f"\n      {order_detail['name']} ✖️ {order_detail['quantity']}\n      Summa: {order_detail['amount']}"
                i += 1
            await state.update_data(index=i, page=page)
            keyboard = await move_keyboard()
            await message.answer(text, reply_markup=keyboard)
        else:
            keyboard = await menu_keyboard()
            text = "Hozircha to'lovlar tarixingiz bo'sh ⚠️"
            await message.answer(text, reply_markup=keyboard)
        await state.set_state('order_history')

    if message.text == "Yangiliklar":
        await state.update_data(new_id=0)
        back_keyboard = await back_key()
        await message.answer("💥 Yangiliklar 👇", reply_markup=back_keyboard)
        news = await get_active_sales_all()
        news = news[0]
        text = f"🔥 {news.name}\n\n{news.description} "
        keyboard = await move_keyboard()
        await message.answer(text, reply_markup=keyboard)
        await state.set_state('news_move')


@dp.message_handler(state="get_comment")
async def get_comment(message: types.Message, state: FSMContext):
    await add_comment(user_id=message.from_user.id, comment=message.text)
    keyboard = await menu_keyboard()
    await message.answer("Murojaatingiz o'rganish uchun mutaxassisimizga yetkazildi\n"
                         "Kerakli bo'limni tanlang", reply_markup=keyboard)
    await state.set_state("user_menu")


@dp.callback_query_handler(state="aksiya")
async def aksiya_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    indexation = int(data['sale_id'])
    sale = await get_active_sales_all()
    if call.data == "enter":
        sale = sale[indexation]
        keyboard = await sale_confirm(sale.id)
        text = f"{sale.name} \nAksiyasiga qo'shilishni istaysizmi"
        await call.message.edit_text(text, reply_markup=keyboard)
        await state.set_state('sale_enter')
        return
    elif call.data == "next":
        indexation = (indexation + 1) % len(sale)
    elif call.data == "back":
        indexation = (indexation - 1) % len(sale)
    sale = sale[indexation]
    text = f"🔥 {sale.name}\n\n 🎁 {sale.description}"
    keyboard = await move_keyboard()
    await state.update_data(sale_id=indexation)
    await call.message.edit_text(text, reply_markup=keyboard)
    await state.set_state('aksiya')


@dp.callback_query_handler(state="news_move")
async def aksiya_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    indexation = int(data['new_id'])
    news = await get_news()
    if call.data == "next":
        indexation = (indexation + 1) % len(news)
    elif call.data == "back":
        indexation = (indexation - 1) % len(news)
    news = news[indexation]
    text = f"🔥 {news.name}\n\n{news.description}"
    keyboard = await move_keyboard()
    await state.update_data(bew_id=indexation)
    await call.message.edit_text(text, reply_markup=keyboard)
    await state.set_state('news_move')


@dp.callback_query_handler(state="order_history")
async def order_history(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    indexation = int(data['index'])
    pagination = int(data['page'])
    text = "🛒 Xaridlaringiz \n"
    user = await get_user(user_id=call.from_user.id)
    if call.data == 'next':
        pagination += 1
        orders = await get_user_orders(phone=user.phone, page=pagination)
        if orders:
            for order in orders:
                datetime_obj = datetime.strptime(order['chequeDate'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                formatted_datetime = datetime_obj.strftime("%d.%m.%Y %H:%M")
                text += f"\n\n{indexation}) 📆 Sana: {formatted_datetime}\n    💲 Jami: {order['totalAmount']}"
                for order_detail in order['products']:
                    text += f"\n      {order_detail['name']} ✖️ {order_detail['quantity']}\n      Summa: {order_detail['amount']}"
                indexation += 1
            await state.update_data(index=indexation, page=pagination)
            keyboard = await move_keyboard()
            await call.message.edit_text(text, reply_markup=keyboard)
        else:
            orders = await get_user_orders(phone=user.phone, page=0)
            page = 0
            if orders:
                i = 1
                for order in orders:
                    datetime_obj = datetime.strptime(order['chequeDate'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                    formatted_datetime = datetime_obj.strftime("%d.%m.%Y %H:%M")
                    text += f"\n\n{i}) 📆 Sana: {formatted_datetime}\n    💲 Jami: {order['totalAmount']}"
                    for order_detail in order['products']:
                        text += f"\n      {order_detail['name']} ✖️ {order_detail['quantity']}\n      Summa: {order_detail['amount']}"
                    i += 1
                await state.update_data(index=i, page=page)
                keyboard = await move_keyboard()
                await call.message.edit_text(text, reply_markup=keyboard)
    if call.data == 'back':
        pagination = pagination - 1 if pagination != 0 else 0
        orders = await get_user_orders(phone=user.phone, page=pagination)
        indexation -= 5
        if orders:
            for order in orders:
                datetime_obj = datetime.strptime(order['chequeDate'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
                formatted_datetime = datetime_obj.strftime("%d.%m.%Y %H:%M")
                text += f"\n\n{indexation}) 📆 Sana: {formatted_datetime}\n    💲 Jami: {order['totalAmount']}"
                for order_detail in order['products']:
                    text += f"\n      {order_detail['name']} ✖️ {order_detail['quantity']}\n      Summa: {order_detail['amount']}"
                indexation += 1
            await state.update_data(index=indexation, page=pagination)
            keyboard = await move_keyboard()
            await call.message.edit_text(text, reply_markup=keyboard)








