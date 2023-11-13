import logging

from aiogram import types
from aiogram.types import InlineKeyboardButton

SUBSCRIPTION_CHANNELS = ["@zahratunuz", "@zahratun_food"]


async def is_subscribed(message: types.Message, chat_id, user_id=None):
    user = message.from_user
    is_subscriber = await message.bot.get_chat_member(chat_id, user.id if user_id is None else user_id)
    logging.info(user.id)
    if is_subscriber and is_subscriber.status in ('member', 'administrator', 'creator'):
        return True
    else:
        return False


async def unsubscribed_channels(message: types.Message, user_id=None):
    new_list = []
    for num, channel in enumerate(SUBSCRIPTION_CHANNELS):
        is_subscription = await is_subscribed(message, channel, user_id)
        if is_subscription is False:
            new_list.append(channel)
    return new_list


async def process_subscription(message: types.Message, user_id=None):
    unsub_channels = await unsubscribed_channels(message, user_id)
    if unsub_channels:
        channel_kb = types.InlineKeyboardMarkup()
        for num, channel in enumerate(unsub_channels):
            channel_kb.add(InlineKeyboardButton(f"{num + 1}-Kanal", url="https://t.me/" + channel.replace('@', '')))
        channel_kb.add(InlineKeyboardButton("Tasdiqlash", callback_data="approve"))

        await message.answer('Ushbu botdan foydalanishu uchun quyidagi kanallarga a\'zo bolish kerak',
                             reply_markup=channel_kb)
        return False
    return True
