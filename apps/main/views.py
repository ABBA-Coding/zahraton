from .models import *
from rest_framework import generics
from apps.telegram_bot.models import *
from .serializers import *
from rest_framework.response import Response


class GetUserView(generics.ListAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer

    def list(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        t_user = TelegramUser.objects.filter(telegram_id=user_id).first()
        data = {
            'status': False
        }
        if t_user:
            data = {
                'status': True,
                'telegram_id': t_user.telegram_id,
                'moneyback_id': t_user.moneyback_id,
                'phone': t_user.phone,
                'full_name': t_user.full_name,
            }
        return Response(data)


class AddUserView(generics.CreateAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer

