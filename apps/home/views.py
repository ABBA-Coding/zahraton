from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic.edit import DeleteView
from apps.main.forms import *
from apps.telegram_bot.models import *
from django.urls import reverse_lazy
import requests
import os
from datetime import datetime
from django.db.models import Q


api_token = str(os.getenv("BOT_TOKEN"))
base_url = f'https://api.telegram.org/bot{api_token}'


def send_notifications(text, chat_id, photo_url):
    url = f'{base_url}/sendPhoto'
    files = {'photo': open(f"/var/www/zahraton.itlink.uz/media/{photo_url}", 'rb')}
    data = {'chat_id': chat_id, 'caption': text}
    response = requests.post(url, files=files, data=data)
    return response.status_code


@login_required(login_url="/login/")
def index(request):

    current_date = datetime.now()
    chats_in_current_month = TelegramChat.objects.filter(
        Q(register_date__year=current_date.year) &
        Q(register_date__month=current_date.month)
    )
    users_in_current_month = TelegramUser.objects.filter(
        Q(register_date__year=current_date.year) &
        Q(register_date__month=current_date.month)
    )

    telegram_chats = TelegramChat.objects.all()
    users = TelegramUser.objects.all()
    context = {
        'segment': 'dashboard',
        'telegram_chats': len(telegram_chats),
        'this_month_chats': len(chats_in_current_month),
        'this_month_users': len(users_in_current_month),
        'users': len(users),
        'cashbacks': []
    }

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def sales_view(request):
    sales = Sale.objects.all().order_by('id')
    search_query = request.GET.get('q')
    if search_query:
        sales = sales.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    paginator = Paginator(sales, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        "segment": "sales"
    }
    html_template = loader.get_template('home/sales.html')
    return HttpResponse(html_template.render(context, request))


def sale_detail(request, pk):
    sale = Sale.objects.get(id=pk)

    if request.method == 'POST':
        form = SaleForm(request.POST, request.FILES, instance=sale)
        if form.is_valid():
            form.save()
            return redirect('sales')
    else:
        form = SaleForm(instance=sale)

    return render(request,
                  'home/sale_detail.html',
                  {'form': form, 'sale': sale, 'segment': 'sales'})


def sale_create(request):
    if request.method == 'POST':
        form = SaleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('sales')
    else:
        form = SaleForm()

    return render(request,
                  'home/sale_create.html',
                  {'form': form})


class SaleDelete(DeleteView):
    model = Sale
    fields = '__all__'
    success_url = reverse_lazy('sales')


@login_required(login_url="/login/")
def news_view(request):
    news = News.objects.all().order_by('id')
    search_query = request.GET.get('q')
    if search_query:
        news = news.filter(Q(name__icontains=search_query) | Q(description__icontains=search_query))
    paginator = Paginator(news, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        "segment": "news"
    }
    html_template = loader.get_template('home/news.html')
    return HttpResponse(html_template.render(context, request))


def news_detail(request, pk):
    news = News.objects.get(id=pk)

    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            form.save()
            return redirect('news')
    else:
        form = NewsForm(instance=news)

    return render(request,
                  'home/news_detail.html',
                  {'form': form, 'news': news, 'segment': 'news'})


def news_create(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('news')
    else:
        form = NewsForm()

    return render(request,
                  'home/news_create.html',
                  {'form': form, 'segment': 'news'})


class NewsDelete(DeleteView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('news')


def notification_create(request):
    if request.method == 'POST':
        form = NotificationForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save()
            chats = TelegramChat.objects.all()
            for i in chats:
                text = instance.description
                image_path = instance.ImageURL
                chat_id = i.telegram_id
                response = send_notifications(text=text, chat_id=chat_id, photo_url=image_path)
                if response == 200:
                    instance.all_chats += 1
            instance.save()
        return redirect('notifications')
    else:
        form = NotificationForm()

    return render(request,
                  'home/notification_create.html',
                  {'form': form})


@login_required(login_url="/login/")
def notifications_view(request):
    notification = Notification.objects.all().order_by('-id')
    paginator = Paginator(notification, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        "segment": "notification"
    }
    html_template = loader.get_template('home/notifications.html')
    return HttpResponse(html_template.render(context, request))

