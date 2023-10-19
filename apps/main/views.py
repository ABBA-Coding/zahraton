from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from .models import *
from rest_framework import generics
from apps.telegram_bot.models import *
from .serializers import *
from rest_framework.response import Response
from django.db.models import Q, Case, When, F, IntegerField

from .tasks import send_notifications_task


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
                'gender': t_user.gender,
                'longitude': t_user.longitude,
                'latitude': t_user.latitude,
                'birth': t_user.birth
            }
        return Response(data)


class AddUserView(generics.CreateAPIView):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer


class AddChatView(generics.CreateAPIView):
    queryset = TelegramChat.objects.all()
    serializer_class = TelegramChatSerializer

    def perform_create(self, serializer):
        # Check if a chat with the same criteria already exists
        chat_criteria = {
            'telegram_id': serializer.validated_data['user_id']
            # Add other criteria as needed
        }
        existing_chat, created = TelegramChat.objects.get_or_create(**chat_criteria)
        existing_chat.is_stopped = False
        existing_chat.save()
        return existing_chat


class NewsListView(generics.ListAPIView):
    serializer_class = NewsListSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        user_info = TelegramUser.objects.filter(telegram_id=user_id).first()
        if user_info:
            age = user_info.age
            gender = user_info.gender
            queryset = News.objects.filter(
                Q(for_gender='Hamma uchun') | Q(for_gender=gender),
                min_age__lte=age,
                max_age__gte=age,
                active=True
            ).prefetch_related("newsshots_set").order_by('-id')

            queryset = queryset.annotate(max_age_adjusted=Case(
                When(max_age=0, then=1000),
                default=F('max_age'),
                output_field=IntegerField()
            ))

            return queryset

        return News.objects.none()


class SaleListView(generics.ListAPIView):
    serializer_class = SaleListSerializer
    queryset = Sale.objects.prefetch_related("saleshots_set").order_by('-id')


def send_telegram(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    media = []
    for i in notification.notificationshots_set.all():
        media.append(i.image.path)
    notification.status = notification.NotificationStatus.PROCEED
    notification.save()
    send_notifications_task.delay(notification_id, notification.description, media)

    return redirect(reverse('admin:main_notification_changelist'))