import base64
import io

from django.conf import settings

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
    image_compress = serializers.SerializerMethodField()

    class Meta:
        model = NewsShots
        fields = "__all__"

    def get_image_compress(self, obj):
        compressed_image = obj.image_compress.url
        cache_path = settings.MEDIA_ROOT
        compressed_image_path = cache_path + compressed_image[len(settings.MEDIA_URL):]

        with open(compressed_image_path, 'rb') as image_file:
            image = Image.open(image_file)
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            byte_io = io.BytesIO()
            image.save(byte_io, format='JPEG', quality=60)  # Adjust the quality as needed
            byte_io.seek(0)
            encoded_string = base64.b64encode(byte_io.read()).decode('utf-8')
            return encoded_string


class NewsListSerializer(serializers.ModelSerializer):
    newsshots_set = NewsShotsSerializer(many=True)

    class Meta:
        model = News
        fields = "__all__"


class SaleShotsSerializer(serializers.ModelSerializer):
    image_compress = serializers.SerializerMethodField()

    class Meta:
        model = SaleShots
        fields = "__all__"

    def get_image_compress(self, obj):
        compressed_image = obj.image_compress.url
        cache_path = settings.MEDIA_ROOT
        compressed_image_path = cache_path + compressed_image[len(settings.MEDIA_URL):]

        with open(compressed_image_path, 'rb') as image_file:
            image = Image.open(image_file)
            if image.mode in ("RGBA", "P"):
                image = image.convert("RGB")
            byte_io = io.BytesIO()
            image.save(byte_io, format='JPEG', quality=60)  # Adjust the quality as needed
            byte_io.seek(0)
            encoded_string = base64.b64encode(byte_io.read()).decode('utf-8')
            return encoded_string


class SaleListSerializer(serializers.ModelSerializer):
    saleshots_set = SaleShotsSerializer(many=True)

    class Meta:
        model = Sale
        fields = "__all__"
