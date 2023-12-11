from django import forms
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import admin
from .forms import CustomCKEditorWidget


from .models import *


class NewsShotsInline(admin.TabularInline):
    extra = 1
    model = NewsShots


class SaleShotsInline(admin.TabularInline):
    extra = 1
    model = SaleShots


class NotificationShotsInline(admin.TabularInline):
    extra = 1
    model = NotificationShots


class NewsModelAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CustomCKEditorWidget())

    class Meta:
        model = News
        fields = '__all__'


class SaleModelAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CustomCKEditorWidget())

    class Meta:
        model = Sale
        fields = '__all__'


class NotificationModelAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CustomCKEditorWidget())

    class Meta:
        model = Notification
        fields = '__all__'


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["short_description", "display_image", "all_chats_count", "created_at", "tools_column"]
    inlines = [NotificationShotsInline]

    form = NotificationModelAdminForm

    def tools_column(self, obj):
        html_tag = "Jarayonda"
        if obj.status == 0:
            html_tag = '<a href="{0}" class="btn btn-success">Boshlash</a> '
        elif obj.status == 1:
            html_tag = 'Yuborildi'
        return mark_safe(
            html_tag.format(
                reverse('send_notification', args=[obj.pk]), )
        )

    tools_column.short_description = 'Boshqaruv'
    tools_column.allow_tags = True

    def short_description(self, obj):
        return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description

    short_description.short_description = "Izoh"

    def all_chats_count(self, obj):
        return obj.all_chats

    all_chats_count.short_description = "Xabar yuborildi"

    def display_image(self, obj):
        images = obj.notificationshots_set
        image = None
        if images.exists():
            image = images.first()
        img_html = f'<img src="{image.image.url}" width="50" height="50" />' if image else '<div>Rasmsiz</div>'
        return mark_safe(img_html)

    display_image.short_description = "Rasmi"

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["name", "short_description", "active", "created_at", "tools_column"]
    inlines = [NewsShotsInline]
    form = NewsModelAdminForm

    def short_description(self, obj):
        return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description

    short_description.short_description = "Izoh"

    def tools_column(self, obj):
        return mark_safe(
            '<a href="{0}" class="btn btn-primary">Tahrirlash</a> '
            '<a href="{1}" class="btn btn-danger">O\'chirish</a>'.format(
                reverse('admin:main_news_change', args=[obj.pk]),
                reverse('admin:main_news_delete', args=[obj.pk])
            ))

    tools_column.short_description = 'Boshqaruv'
    tools_column.allow_tags = True


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ["name", "short_description", "active", "created_at", "tools_column"]
    inlines = [SaleShotsInline]
    form = SaleModelAdminForm

    def short_description(self, obj):
        return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description

    short_description.short_description = "Izoh"

    def tools_column(self, obj):
        return mark_safe(
            '<a href="{0}" class="btn btn-primary">Tahrirlash</a> '
            '<a href="{1}" class="btn btn-danger">O\'chirish</a>'.format(
                reverse('admin:main_sale_change', args=[obj.pk]),
                reverse('admin:main_sale_delete', args=[obj.pk])
            ))

    tools_column.short_description = 'Boshqaruv'
    tools_column.allow_tags = True
