from django.urls import path
from apps.home import views

urlpatterns = [
    path('', views.index, name='home'),
    path('sales/', views.sales_view, name='sales'),
    path('sales_update/<int:pk>', views.sale_detail, name='sale_update'),
    path('sales_delete/<int:pk>', views.SaleDelete.as_view(), name='sale_delete'),
    path('sale_create/', views.sale_create, name='sale_create'),
    path('news/', views.news_view, name='news'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('notification_create/', views.notification_create, name='notification_create'),
    path('news_update/<int:pk>', views.news_detail, name='news_update'),
    path('news_create/', views.news_create, name='news_create'),
    path('news_delete/<int:pk>', views.NewsDelete.as_view(), name='news_delete'),
]

