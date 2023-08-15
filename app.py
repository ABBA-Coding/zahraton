import os
import django
from loader import bot
from aiogram.utils import executor
from aiogram.utils.executor import start_webhook
from data import config


WEBHOOK_HOST = config.HOST_URL
WEBHOOK_PATH = '/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip
WEBAPP_PORT = os.getenv('PORT', default=8000)


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    print("Bot started")


async def on_shutdown(dp):
    print("Bot stopped")
    await bot.delete_webhook()

    await dp.storage.close()
    await dp.storage.wait_closed()


def setup_django():
    os.environ.setdefault(
        "DJANGO_SETTINGS_MODULE",
        "core.settings"
    )
    os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})
    django.setup()


if __name__ == '__main__':
    # executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
    setup_django()
    from handlers import dp
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
