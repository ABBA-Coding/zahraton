import os
import django


async def on_startup(dp):
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)

    
async def on_shutdown(dp):
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
    setup_django()

    from aiogram.utils import executor
    from loader import bot
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
