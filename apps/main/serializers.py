from rest_framework import serializers
from .models import *
from apps.telegram_bot.models import *


class TelegramUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = TelegramUser
        fields = '__all__'

