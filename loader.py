from aiogram import Bot, Dispatcher, types
from data import config
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware

from utils.db_api.database import Database

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = RedisStorage2(port=6379)
dp = Dispatcher(bot, storage=storage)
db = Database()
DEBUG = False


class EnvironmentMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ["error", "update"]

    def __init__(self, **kwargs):
        super().__init__()
        self.kwargs = kwargs

    async def pre_process(self, obj, data, *args):
        data.update(**self.kwargs)


dp.setup_middleware(EnvironmentMiddleware(db=db, debug=DEBUG))

if DEBUG is False:
    import sentry_sdk
    from sentry_sdk.integrations.asyncio import AsyncioIntegration

    sentry_sdk.init(dsn="https://02bc94e0e1973408152f6632cc6ac5ab@o4504621259948032.ingest.sentry.io/4506027009572864",
                    integrations=[AsyncioIntegration()])
