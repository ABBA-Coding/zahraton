from rest_framework import serializers
from .models import *
from apps.telegram_bot.models import *


class TelegramUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'

    def create(self, validated_data):
        telegram_id = validated_data.get('telegram_id')
        existing_user = TelegramUser.objects.filter(telegram_id=telegram_id)
        if existing_user.exists():
            existing_user.delete()
        return TelegramUser.objects.create(**validated_data)


class TelegramChatSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()


class NewsShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsShots
        fields = "__all__"


class NewsListSerializer(serializers.ModelSerializer):
    newsshots_set = NewsShotsSerializer(many=True)

    class Meta:
        model = News
        fields = "__all__"


class SaleShotsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleShots
        fields = "__all__"


class SaleListSerializer(serializers.ModelSerializer):
    saleshots_set = SaleShotsSerializer(many=True)

    class Meta:
        model = Sale
        fields = "__all__"
