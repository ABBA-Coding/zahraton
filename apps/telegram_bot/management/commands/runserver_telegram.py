from django.core.management.base import BaseCommand
from aiogram import Bot, Dispatcher, executor
from apps.telegram_bot.handlers import dp


class Command(BaseCommand):
    help = 'Starts Django and aiogram bot simultaneously'

    def handle(self, *args, **options):
        # Start Django
        # from django.core.management import call_command
        # call_command('runserver')
        
        # Start aiogram bot
        executor.start_polling(dp, skip_updates=True)

