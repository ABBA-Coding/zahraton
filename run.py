from aiogram import Dispatcher


async def on_startup(dp: Dispatcher):
    from utils.set_bot_commands import set_default_commands
    await set_default_commands(dp)


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    from aiogram.utils import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)
