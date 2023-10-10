from django.contrib import admin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.safestring import mark_safe

from apps.home.tasks import send_notifications_task

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


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ["short_description", "display_image", "status", "all_chats_count"]
    inlines = [NotificationShotsInline]

    def short_description(self, obj):
        return obj.description[:100] + "..." if len(obj.description) > 100 else obj.description

    short_description.short_description = "Izoh"

    def all_chats_count(self, obj):
        return obj.all_chats

    all_chats_count.short_description = "Xabar yuborildi"

    def display_image(self, obj):
        images = obj.notificationshots_set

        return mark_safe(
            '<img src="{}" width="50" height="50" />'.format(
                images.first().image.url if images.exists() else 'static/img/icons/icon-48x48.png'
            ))

    display_image.short_description = "Rasmi"

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@receiver(post_save, sender=Notification)
def run_celery_task_on_create(sender, instance, created, **kwargs):
    if created:
        # Call your Celery task function here
        send_notifications_task.delay(instance.id)


# Register the signal handler
post_save.connect(run_celery_task_on_create, sender=Notification)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ["name", "short_description", "active", "tools_column"]
    inlines = [NewsShotsInline]

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
    list_display = ["name", "short_description", "active", "tools_column"]
    inlines = [SaleShotsInline]

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
