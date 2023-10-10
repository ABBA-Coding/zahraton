from django.urls import path
from .views import *


urlpatterns = [
    path('get_user/', GetUserView.as_view(), name='get_user'),
    path('post_user/', AddUserView.as_view(), name='post_user'),
    path('add_chat/', AddChatView.as_view(), name="add_chat"),
    path('news/', NewsListView.as_view(), name="news_list"),
    path('sales/', SaleListView.as_view(), name="sale_list"),
]