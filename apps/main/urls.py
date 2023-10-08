from django.urls import path
from .views import *


urlpatterns = [
    path('get_user/', GetUserView.as_view(), name='get_user'),
    path('post_user/', AddUserView.as_view(), name='post_user'),

]