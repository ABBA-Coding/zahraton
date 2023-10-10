from datetime import datetime

from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import dp, bot
from keyboards.inline.menu_button import *
from keyboards.inline.main_inline import *
from utils.db_api.database import *
import qrcode
from aiogram.types import ReplyKeyboardRemove


async def get_sales_by_index(m: types.Message, index: int, db: Database, debug: bool, wait_msg: types.Message,
                             next: bool = False):
    sale = await db.get_active_sales_all()
    if next:
        index = abs(index + 1) % (len(sale[0]) if len(sale[0]) != 0 else 1)

    if sale:
        sale = sale[0]
        if sale:
            sale = sale[index]
            text = f"🔥 {sale['name']}\n\n 🎁{sale['description']} "

            if sale["saleshots_set"]:
                media_group = []
                for sale_obj in sale['saleshots_set']:
                    photo = (open(f"{sale_obj['image'].replace('http://localhost:8000/', '')}", 'rb') if debug is True
                             else open(
                        f"{sale_obj['image'].replace('https://botloyalty.zahratun.uz/', '/var/www/zahraton.itlink.uz/')}",
                        'rb'))
                    media_group += [
                        types.InputMediaPhoto(media=photo, caption=text),
                    ]
                    text = None
                await m.answer_media_group(media=media_group)
            else:
                await m.answer(text)
            await wait_msg.delete()
            return index


async def get_news_by_index(m: types.Message, index: int, db: Database, debug: bool, wait_msg: types.Message,
                            next: bool = False):
    news = await db.get_news(m.from_user.id)
    if next:
        index = abs(index + 1) % (len(news[0]) if len(news[0]) != 0 else 1)

    if news:
        news = news[0]
        if news:
            news = news[index]
            text = f"🔥 {news['name']}\n\n 🎁{news['description']} "

            if news["newsshots_set"]:
                media_group = []
                for sale_obj in news['newsshots_set']:
                    photo = (open(f"{sale_obj['image'].replace('http://localhost:8000/', '')}", 'rb') if debug is True
                             else open(
                        f"{sale_obj['image'].replace('https://botloyalty.zahratun.uz/', '/var/www/zahraton.itlink.uz/')}",
                        'rb'))
                    media_group += [
                        types.InputMediaPhoto(media=photo, caption=text),
                    ]
                    text = None
                await bot.send_media_group(chat_id=m.from_user.id, media=media_group)
            else:
                await m.answer(text)
            await wait_msg.delete()
            return index


@dp.message_handler(state='user_menu')
async def menu(message: types.Message, state: FSMContext, debug: bool, db: Database):
    await state.update_data(action='menu')

    if message.text == "💰 Mening hisobim (bonuslarim)":
        user = await db.get_user(user_id=message.from_user.id)
        keyboard = menu_keyboard()
        cashbacks = await db.get_user_balance(user['phone'])
        formatted_total = "{:,.3f}".format(float(cashbacks['balance']) / 1000).replace(",", ".") if cashbacks[
                                                                                                        'balance'] >= 1000 else int(
            cashbacks['balance'])
        text = f"\n\n💵 Hozirgi keshbek: <b>{formatted_total}</b> UZS"
        await message.answer(text, reply_markup=keyboard)
    if message.text == "🎁 Aksiyalar":
        await state.update_data(sale_id=0)
        await message.answer("Hozirda aktiv bo'lgan aksiyalar 👇", reply_markup=move_reply_keyboard())
        wait_msg = await message.answer(text='⏳')
        await state.set_state('aksiya')
        await get_sales_by_index(message, 0, db, debug, wait_msg)
    if message.text == "📰 Yangiliklar":
        await state.update_data(new_id=0)
        await message.answer("💥 Yangiliklar 👇", reply_markup=move_reply_keyboard())
        wait_msg = await message.answer(text='⏳')
        await state.set_state('news_move')
        await get_news_by_index(message, 0, db, debug, wait_msg)

    if message.text == "📝 Taklif va shikoyatlar":
        keyboard = back_key()
        await message.answer("Iltimos taklif va shikoyatlaringiz haqida imkon boricha batafsil so‘zlab bering "
                             "va zarur bo‘lsa surat jo‘nating)\n\nHar bir taklif va shikoyatingiz biz uchun juda "
                             "katta ahamiyatga ega. Xabaringiz javobsiz qolmaydi.",
                             reply_markup=keyboard)
        await state.set_state("get_comment")
    if message.text == '🔄 QR kod':
        user = await db.get_user(user_id=message.from_user.id)
        balance = await db.get_user_balance(user['phone'])
        user_uuid = await db.get_api_uuid(user['phone'])
        q = qrcode.make(f'{user_uuid}')
        q.save('qrcode.png')
        keyboard = menu_keyboard()
        photo = open('qrcode.png', 'rb')
        formatted_total = ("{:,.3f}".format(float(balance['balance']) / 1000).replace(",", ".") if
                           balance['balance'] >= 1000 else int(balance['balance']))

        await message.answer_photo(photo=photo, caption=f"Sizning keshbekingizni ishlatish uchun QR kodingiz "
                                                        f"👆\n\n💵 Hozirgi keshbekingiz: <b>{formatted_total}</b> UZS",
                                   reply_markup=keyboard)
    if message.text == "💳 To'lovlar tarixi":
        await message.answer(text='⏳', reply_markup=ReplyKeyboardRemove())
        user = await db.get_user(message.from_user.id)
        years = await db.get_user_orders(user['phone'])
        await bot.delete_message(chat_id=message.from_user.id, message_id=message.message_id + 1)
        markup = year_keyboard(years)
        await message.answer(text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.set_state('get_year_')


@dp.message_handler(state="get_comment", content_types=types.ContentType.ANY)
async def get_comment(message: types.Message, state: FSMContext, db: Database):
    user = await db.get_user(message.from_user.id)
    if message.photo:
        photo = message.photo[-1].file_id
        await state.update_data(photo_id=photo)
        if message.caption:
            text = ''
            text += f"👤 Mijoz: {user['full_name']}\n"
            text += f"👤 Profil: @{message.from_user.username}\n" if message.from_user.username is not None else f"👤 Profil: T.me/+{user['phone']}\n"
            text += f"📞 Telefon raqam: +{user['phone']}\n"
            text += f"\n✍️ Xabar: <b>{message.caption}</b>"
            keyboard = menu_keyboard()
            await bot.send_photo(photo=photo, chat_id=-1001669827084, caption=text)
            await message.answer("Murojaatingiz o'rganish uchun mutaxassisimizga yetkazildi\n"
                                 "Kerakli bo'limni tanlang", reply_markup=keyboard)
            await state.set_state("user_menu")
        else:
            keyboard = comment_keyboard(type='text')
            await message.answer(text="Xarabringizga izoh qo'shishni istaysizmi?", reply_markup=keyboard)
            await state.set_state('get_comment_caption')
    if message.text:
        await state.update_data(comment_text=message.text)
        keyboard = comment_keyboard(type='photo')
        await message.answer(text="Xabaringizga rasm qo'shishni istaysizmi?", reply_markup=keyboard)
        await state.set_state('get_comment_photo')


@dp.message_handler(state="get_comment_caption", content_types=types.ContentType.TEXT)
async def get_comment_last(message: types.Message, state: FSMContext, db: Database):
    user = await db.get_user(message.from_user.id)
    if message.text == "✅ Jo'natish":
        data = await state.get_data()
        photo = data['photo_id']
        text = ''
        text += f"👤 Mijoz: {user['full_name']}\n"
        text += f"👤 Profil: @{message.from_user.username}\n" if message.from_user.username is not None else f"👤 Profil: T.me/+{user['phone']}\n"
        text += f"📞 Telefon raqam: +{user['phone']}\n"
        keyboard = menu_keyboard()
        await bot.send_photo(photo=photo, chat_id=-1001669827084, caption=text)
        await message.answer("Murojaatingiz o'rganish uchun mutaxassisimizga yetkazildi\n"
                             "Kerakli bo'limni tanlang", reply_markup=keyboard)
        await state.set_state("user_menu")
    if message.text == "✍️ Izoh qo'shish":
        keyboard = back_key()
        await message.answer(text="Xabaringizni yuboring", reply_markup=keyboard)
        await state.set_state('get_comment_caption_photo')


@dp.message_handler(state="get_comment_photo", content_types=types.ContentType.TEXT)
async def get_comment_last2(message: types.Message, state: FSMContext, db: Database):
    user = await db.get_user(message.from_user.id)
    if message.text == "✅ Jo'natish":
        data = await state.get_data()
        comment = data['comment_text']
        text = ''
        text += f"👤 Mijoz: {user['full_name']}\n"
        text += f"👤 Profil: @{message.from_user.username}\n" if message.from_user.username is not None else f"👤 Profil: T.me/+{user['phone']}\n"
        text += f"📞 Telefon raqam: +{user['phone']}\n"
        text += f"\n✍️ Xabar: <b>{comment}</b>"
        keyboard = menu_keyboard()
        await bot.send_message(chat_id=-1001669827084, text=text)
        await message.answer("Murojaatingiz o'rganish uchun mutaxassisimizga yetkazildi\n"
                             "Kerakli bo'limni tanlang", reply_markup=keyboard)
        await state.set_state("user_menu")
    if message.text == "🖼 Rasm qo'shish":
        keyboard = back_key()
        await message.answer(text="Rasmni yuboring", reply_markup=keyboard)
        await state.set_state('get_comment_caption_photo')


@dp.message_handler(state="get_comment_caption_photo", content_types=types.ContentType.PHOTO)
async def get_comment_last3(message: types.Message, state: FSMContext, db: Database):
    user = await db.get_user(message.from_user.id)
    photo = message.photo[-1].file_id
    data = await state.get_data()
    comment = data['comment_text']
    await state.update_data(photo_id=photo)
    text = ''
    text += f"👤 Mijoz: {user['full_name']}\n"
    text += f"👤 Profil: @{message.from_user.username}\n" if message.from_user.username is not None else f"👤 Profil: T.me/+{user['phone']}\n"
    text += f"📞 Telefon raqam: +{user['phone']}\n"
    text += f"\n✍️ Xabar: <b>{comment}</b>"
    keyboard = menu_keyboard()
    await bot.send_photo(photo=photo, chat_id=-1001669827084, caption=text)
    await message.answer("Murojaatingiz o'rganish uchun mutaxassisimizga yetkazildi\n"
                         "Kerakli bo'limni tanlang", reply_markup=keyboard)
    await state.set_state("user_menu")


@dp.message_handler(state="get_comment_caption_photo", content_types=types.ContentType.TEXT)
async def get_comment_last4(message: types.Message, state: FSMContext, db: Database):
    user = await db.get_user(message.from_user.id)
    data = await state.get_data()
    photo = data['photo_id']
    caption = message.text
    text = ''
    text += f"👤 Mijoz: {user['full_name']}\n"
    text += f"👤 Profil: @{message.from_user.username}\n" if message.from_user.username is not None else f"👤 Profil: T.me/+{user['phone']}\n"
    text += f"📞 Telefon raqam: +{user['phone']}\n"
    text += f"\n✍️ Xabar: <b>{caption}</b>"
    keyboard = menu_keyboard()
    await bot.send_photo(photo=photo, chat_id=-1001669827084, caption=text)
    await message.answer("Murojaatingiz o'rganish uchun mutaxassisimizga yetkazildi\n"
                         "Kerakli bo'limni tanlang", reply_markup=keyboard)
    await state.set_state("user_menu")


@dp.message_handler(state="aksiya")
async def aksiya_handler(m: types.Message, state: FSMContext, db: Database, debug: bool):
    data = await state.get_data()
    indexation = int(data['sale_id'])
    if m.text == "Keyingi ➡️":
        wait_msg = await m.answer(text='⏳')
        indexation = await get_sales_by_index(m, indexation, db, debug, wait_msg, next=True)
        await state.update_data(sale_id=indexation)
        return

    await state.set_state('aksiya')


@dp.message_handler(state="news_move")
async def news_handler(m: types.Message, state: FSMContext, debug: bool, db: Database):
    data = await state.get_data()
    indexation = int(data['new_id'])
    if m.text == "Keyingi ➡️":
        wait_msg = await m.answer(text='⏳')
        indexation = await get_news_by_index(m, indexation, db, debug, wait_msg, next=True)
        await state.update_data(new_id=indexation)
        return
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
async def get_year(call: types.CallbackQuery, state: FSMContext, db: Database):
    data = call.data
    if data != 'back_menu':
        user = await db.get_user(call.from_user.id)
        dates = await db.get_order_month(phone=user['phone'], year=data)
        markup = await month_keyboard(dates)
        await call.message.edit_text(text='Kerakli oyni tanlang 👇', reply_markup=markup)
        await state.update_data(year=data)
        await state.set_state('get_month_')
    else:
        await call.message.delete()
        markup = menu_keyboard()
        await state.finish()
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli buyruqni tanlang 👇', reply_markup=markup)
        await state.set_state('user_menu')


@dp.callback_query_handler(state="get_month_")
async def get_year(call: types.CallbackQuery, state: FSMContext, db: Database):
    data = call.data
    state_data = await state.get_data()
    if data != 'back_menu':
        await call.message.delete()
        user = await db.get_user(call.from_user.id)
        orders = await db.get_orders_by_month(phone=user['phone'], year=state_data["year"], month=data)
        i = 1
        for order in orders:
            text = ''
            datetime_obj = datetime.strptime(order['chequeDate'].split('.')[0], "%Y-%m-%dT%H:%M:%S")
            formatted_datetime = datetime_obj.strftime("%d.%m.%Y %H:%M")
            text += f"\n\n{i}) 📆 <b>Sana</b>: {formatted_datetime}\n"
            for order_detail in order['products']:
                formatted_amount = "{:,.3f}".format(float(order_detail['amount']) / 1000).replace(",", ".") if \
                    order_detail['amount'] >= 1000 else int(order_detail['amount'])

                text += f"\n🛒 {order_detail['name']} ✖️ {order_detail['quantity']} = <b>{formatted_amount}</b> UZS\n"
            formatted_total = "{:,.3f}".format(float(order['totalAmount']) / 1000).replace(",", ".") if order[
                                                                                                            'totalAmount'] >= 1000 else int(
                order['totalAmount'])
            formatted_bonus = "{:,.3f}".format(float(order['writeOff']) / 1000).replace(",", ".") if order[
                                                                                                         'writeOff'] >= 1000 else int(
                order['writeOff'])
            text += f"\n\n💲 <b>Jami</b>: <b>{formatted_total}</b> UZS" \
                    f"\n💳 <b>Bonus orqali to'langan summa</b>: {formatted_bonus} UZS\n"
            i += 1
            chunks = [text[i:i + 4096] for i in range(0, len(text), 4096)]
            for chunk in chunks:
                await bot.send_message(chat_id=call.from_user.id, text=chunk)
        years = await db.get_user_orders(user['phone'])
        markup = year_keyboard(years)
        await bot.send_message(chat_id=call.from_user.id, text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.set_state('get_year_')
    else:
        user = await db.get_user(call.from_user.id)
        years = await db.get_user_orders(user['phone'])
        markup = year_keyboard(years)
        await call.message.edit_text(text='Kerakli yilni tanlang 👇', reply_markup=markup)
        await state.set_state('get_year_')
