from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic.edit import DeleteView
from apps.main.forms import *
from django.urls import reverse_lazy


@login_required(login_url="/login/")
def index(request):
    context = {
        'segment': 'dashboard',
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