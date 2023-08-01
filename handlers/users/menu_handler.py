from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.menu_button import *
from keyboards.inline.main_inline import *
from utils.db_api.database import *
import qrcode
from aiogram.types import InputFile


@dp.message_handler(state='user_menu')
async def menu(message: types.Message, state: FSMContext):
    await state.update_data(action='menu')
    user = await get_user(user_id=message.from_user.id)
    if message.text == "Mening hisobim/Bonuslarim":
        keyboard = await menu_keyboard()
        cashbacks = await get_user_balance(user.phone)
        formatted_total = "{:,.3f}".format(float(cashbacks['balance']) / 1000).replace(",", ".") if cashbacks['balance'] >= 1000 else int(cashbacks['balance'])
        text = f"\n\n💵 Hozirgi keshbek: <b>{formatted_total}</b> UZS"
        await message.answer(text, reply_markup=keyboard)
    if message.text == "Joriy aksiyalar":
        await state.update_data(sale_id=0)
        back_keyboard = await back_key()
        await message.answer("Hozirda aktiv bo'lgan aksiyalar 👇", reply_markup=back_keyboard)
        sale = await get_active_sales_all()
        await state.set_state('aksiya')
        if sale:
            sale = sale[0]
            print("Sale image URL", sale.ImageURL)
            text = f"🔥 {sale.name}\n\n 🎁{sale.description} "
            keyboard = await move_keyboard()
            photo = open(f"{sale.ImageURL}", 'rb')
            await message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)
    if message.text == "Taklif va shikoyatlar":
        keyboard = await back_key()
        await message.answer("Iltimos taklif va shikoyatlaringiz haqida imkon boricha batafsil so‘zlab bering "
                             "va zarur bo‘lsa surat jo‘nating)\n\nHar bir taklif va shikoyatingiz biz uchun juda "
                             "katta ahamiyatga ega. Xabaringiz javobsiz qolmaydi.",
                             reply_markup=keyboard)
        await state.set_state("get_comment")
    if message.text == 'QrCode':
        balance = await get_user_balance(user.phone)
        user_uuid = get_api_uuid(user.phone)
        q = qrcode.make(f'{user_uuid}')
        q.save('qrcode.png')
        keyboard = await menu_keyboard()
        photo = open('qrcode.png', 'rb')
        formatted_total = "{:,.3f}".format(float(balance['balance']) / 1000).replace(",", ".") if balance['balance'] >= 1000 else int(balance['balance'])

        await message.answer_photo(photo=photo, caption=f"Sizning keshbekingizni ishlatish uchun QR kodingiz "
                                                        f"👆\n\n💵 Hozirgi keshbekingiz: <b>{formatted_total}</b> UZS",
                                   reply_markup=keyboard)
    if message.text == "To'lovlar tarixi":
        await message.answer(text='⏳', reply_markup=ReplyKeyboardRemove())
        user = await get_user(message.from_user.id)
        await get_user_orders(phone=user.phone)
        years = await get_order_years(user.phone)
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
        markup = await year_keyboard(years)
        await message.answer(text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.set_state('get_year_')
        # page = 0
        # text = "To'lovlar tarixi bo'limi\n"
        # back_keyboard = await back_key()
        # await message.answer(text, reply_markup=back_keyboard)
        # if orders:
        #     text = ''
        #     i = 1
        #     for order in orders:
        #         datetime_obj = datetime.strptime(order['chequeDate'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
        #         formatted_datetime = datetime_obj.strftime("%d.%m.%Y %H:%M")
        #         text += f"\n\n{i}) 📆 Sana: {formatted_datetime}\n    💲 Jami: {order['totalAmount']}" \
        #                 f"\n    ❇️ Bonus orqali to'langan summa: {order['writeOff']}"
        #         for order_detail in order['products']:
        #             text += f"\n      {order_detail['name']} ✖️ {order_detail['quantity']}\n      Summa: {order_detail['amount']}"
        #         i += 1
        #     await state.update_data(index=i, page=page, back_index=1, len_last_orders=len(orders))
        #     keyboard = await move_keyboard()
        #     try:
        #         await message.answer(text, reply_markup=keyboard)
        #     except:
        #         await message.answer(text[:4000])
        #         await message.answer(text[4000:], reply_markup=keyboard)
        #
        #     await state.set_state('order_history')
        # else:
        #     keyboard = await menu_keyboard()
        #     text = "Hozircha to'lovlar tarixingiz bo'sh ⚠️"
        #     await message.answer(text, reply_markup=keyboard)
        #     await state.set_state('user_menu')

    if message.text == "Yangiliklar":
        await state.update_data(new_id=0)
        back_keyboard = await back_key()
        await message.answer("💥 Yangiliklar 👇", reply_markup=back_keyboard)
        news = await get_news(message.from_user.id)
        await state.set_state('news_move')
        if news:
            news = news[0]
            text = f"🔥 {news.name}\n\n{news.description} "
            keyboard = await move_keyboard()
            photo = open(f"{news.ImageURL}", 'rb')
            await message.answer_photo(photo=photo, caption=text, reply_markup=keyboard)


@dp.message_handler(state="get_comment")
async def get_comment(message: types.Message, state: FSMContext):
    # await add_comment(user_id=message.from_user.id, comment=message.text)
    user = await get_user(message.from_user.id)
    text = ''
    if message.text:
        text += f"👤 Telefon raqam: +{message.from_user.username}\n" if message.from_user.username is not None else f"👤 Telefon raqam: T.me/+{user.phone}\n"
        text += f"👤 Telefon raqam: +{user.phone}\n✍️ Xabar: <b>{message.text}</b>"
    else:
        text += f"👤 Telefon raqam: +{message.from_user.username}\n" if message.from_user.username is not None else f"👤 Telefon raqam: T.me/+{user.phone}\n"
    if message.photo:
        photo = message.photo[-1].file_id
        await bot.send_photo(photo=photo, chat_id=-1001669827084, caption=text)

    else:
        await bot.send_message(chat_id=-1001669827084, text=text)

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
    photo = open(f"{sale.ImageURL}", 'rb')
    text = f"🔥 {sale.name}\n\n 🎁 {sale.description}"
    keyboard = await move_keyboard()
    await state.update_data(sale_id=indexation)
    await bot.edit_message_media(media=types.InputMediaPhoto(media=InputFile(photo)),
                                 chat_id=call.from_user.id,
                                 message_id=call.message.message_id)
    await bot.edit_message_caption(chat_id=call.from_user.id,
                                   message_id=call.message.message_id,
                                   caption=text,
                                   reply_markup=keyboard)
    await state.set_state('aksiya')


@dp.callback_query_handler(state="news_move")
async def news_handler(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    indexation = int(data['new_id'])
    news = await get_news(call.from_user.id)
    if call.data == "next":
        indexation = (indexation + 1) % len(news)
    elif call.data == "back":
        indexation = (indexation - 1) % len(news)
    news = news[indexation]
    await state.update_data(new_id=indexation)
    photo = open(f"{news.ImageURL}", 'rb')
    text = f"🔥 {news.name}\n\n{news.description}"
    keyboard = await move_keyboard()
    await bot.edit_message_media(media=types.InputMediaPhoto(media=InputFile(photo)),
                                 chat_id=call.from_user.id,
                                 message_id=call.message.message_id)
    await bot.edit_message_caption(chat_id=call.from_user.id,
                                   message_id=call.message.message_id,
                                   caption=text,
                                   reply_markup=keyboard)
    await state.set_state('news_move')

# @dp.callback_query_handler(state="order_history")
# async def order_history(call: types.CallbackQuery, state: FSMContext):
#     try:
#         await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id-1)
#     except:
#         pass
#
#     data = await state.get_data()
#     indexation = int(data['index'])
#     len_last_orders = data['len_last_orders']
#     pagination = int(data['page'])
#     text = "🛒 Xaridlaringiz \n"
#     user = await get_user(user_id=call.from_user.id)
#     if call.data == 'next':
#         pagination += 1
#         orders = await get_user_orders(phone=user.phone, page=pagination)
#         if orders:
#             for order in orders:
#                 datetime_obj = datetime.strptime(order['chequeDate'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
#                 formatted_datetime = datetime_obj.strftime("%d.%m.%Y %H:%M")
#                 text += f"\n\n{indexation}) 📆 Sana: {formatted_datetime}\n    💲 Jami: {order['totalAmount']}" \
#                         f"\n    ❇️ Bonus orqali to'langan summa: {order['writeOff']}"
#                 for order_detail in order['products']:
#                     text += f"\n      {order_detail['name']} ✖️ {order_detail['quantity']}\n      Summa: {order_detail['amount']}"
#                 indexation += 1
#             back_index = indexation - int(len_last_orders) - int(len(orders))
#             keyboard = await move_keyboard()
#             try:
#                 await call.message.edit_text(text, reply_markup=keyboard)
#             except:
#                 await call.message.delete()
#                 await bot.send_message(chat_id=call.from_user.id, text=text[:4000])
#                 await bot.send_message(chat_id=call.from_user.id, text=text[4000:], reply_markup=keyboard)
#
#             await state.update_data(index=indexation, page=pagination, back_index=back_index,
#                                     len_last_orders=len(orders))
#         else:
#             orders = await get_user_orders(phone=user.phone, page=0)
#             page = 0
#             if orders:
#                 i = 1
#                 for order in orders:
#                     datetime_obj = datetime.strptime(order['chequeDate'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
#                     formatted_datetime = datetime_obj.strftime("%d.%m.%Y %H:%M")
#                     text += f"\n\n{i}) 📆 Sana: {formatted_datetime}\n    💲 Jami: {order['totalAmount']}" \
#                             f"\n    ❇️ Bonus orqali to'langan summa: {order['writeOff']}"
#                     for order_detail in order['products']:
#                         text += f"\n      {order_detail['name']} ✖️ {order_detail['quantity']}\n      Summa: {order_detail['amount']}"
#                     i += 1
#                 back_index = indexation - int(len_last_orders) - int(len(orders))
#                 keyboard = await move_keyboard()
#                 try:
#                     await call.message.edit_text(text, reply_markup=keyboard)
#                 except:
#                     await call.message.delete()
#                     await bot.send_message(chat_id=call.from_user.id, text=text[:4000])
#                     await bot.send_message(chat_id=call.from_user.id, text=text[4000:], reply_markup=keyboard)
#                 await state.update_data(index=indexation, page=pagination, back_index=back_index,
#                                         len_last_orders=len(orders))
#     if call.data == 'back':
#         pagination = pagination - 1 if pagination != 0 else 0
#         orders = await get_user_orders(phone=user.phone, page=pagination)
#         indexation = int(data['back_index']) if pagination != 0 else 1
#         if orders:
#             for order in orders:
#                 datetime_obj = datetime.strptime(order['chequeDate'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
#                 formatted_datetime = datetime_obj.strftime("%d.%m.%Y %H:%M")
#                 text += f"\n\n{indexation}) 📆 Sana: {formatted_datetime}\n    💲 Jami: {order['totalAmount']}" \
#                         f"\n    ❇️ Bonus orqali to'langan summa: {order['writeOff']}"
#                 for order_detail in order['products']:
#                     text += f"\n      {order_detail['name']} ✖️ {order_detail['quantity']}\n      Summa: {order_detail['amount']}"
#                 indexation += 1
#             back_index = indexation - int(len_last_orders) - int(len(orders))
#             keyboard = await move_keyboard()
#             try:
#                 await call.message.edit_text(text, reply_markup=keyboard)
#             except:
#                 await call.message.delete()
#                 await bot.send_message(chat_id=call.from_user.id, text=text[:4000])
#                 await bot.send_message(chat_id=call.from_user.id, text=text[4000:], reply_markup=keyboard)
#             await state.update_data(index=indexation, page=pagination, back_index=back_index,
#                                     len_last_orders=len(orders))
#


@dp.callback_query_handler(state="get_year_")
async def get_year(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    if data != 'back_menu':
        user = await get_user(call.from_user.id)
        dates = await get_order_month(phone=user.phone, year=data)
        markup = await month_keyboard(dates)
        await call.message.edit_text(text='Kerakli oyni tanlang 👇', reply_markup=markup)
        await state.update_data(year=data)
        await state.set_state('get_month_')
    else:
        await call.message.delete()
        markup = await menu_keyboard()
        await state.finish()
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli buyruqni tanlang 👇', reply_markup=markup)
        await state.set_state('user_menu')


@dp.callback_query_handler(state="get_month_")
async def get_year(call: types.CallbackQuery, state: FSMContext):
    data = call.data
    state_data = await state.get_data()
    if data != 'back_menu':
        await call.message.delete()
        user = await get_user(call.from_user.id)
        orders = await get_orders_by_month(phone=user.phone, year=state_data["year"], month=data)
        i = 1
        for order in orders:
            text = ''
            datetime_obj = datetime.strptime(order['chequeDate'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            formatted_datetime = datetime_obj.strftime("%d.%m.%Y %H:%M")
            text += f"\n\n{i}) 📆 <b>Sana</b>: {formatted_datetime}\n"
            for order_detail in order['products']:
                formatted_amount = "{:,.3f}".format(float(order_detail['amount']) / 1000).replace(",", ".") if order_detail['amount'] >= 1000 else int(order_detail['amount'])

                text += f"\n🛒 {order_detail['name']} ✖️ {order_detail['quantity']} = <b>{formatted_amount}</b> UZS\n"
            formatted_total = "{:,.3f}".format(float(order['totalAmount']) / 1000).replace(",", ".") if order['totalAmount'] >= 1000 else int(order['totalAmount'])
            formatted_bonus = "{:,.3f}".format(float(order['writeOff']) / 1000).replace(",", ".") if order['writeOff'] >= 1000 else int(order['writeOff'])
            text += f"\n\n💲 <b>Jami</b>: <b>{formatted_total}</b> UZS" \
                    f"\n💳 <b>Bonus orqali to'langan summa</b>: {formatted_bonus} UZS\n"
            i += 1
            chunks = [text[i:i+4096] for i in range(0, len(text), 4096)]
            for chunk in chunks:
                await bot.send_message(chat_id=call.from_user.id, text=chunk)
        years = await get_order_years(user.phone)
        markup = await year_keyboard(years)
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.set_state('get_year_')
    else:
        user = await get_user(call.from_user.id)
        await get_user_orders(phone=user.phone)
        years = await get_order_years(user.phone)
        markup = await year_keyboard(years)
        await call.message.edit_text(text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.set_state('get_year_')
