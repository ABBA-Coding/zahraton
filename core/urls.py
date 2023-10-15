from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/admin'), name="home"),
    # path('admin/logout', RedirectView.as_view(url='/admin')),

    # API endpoints
    path("api/", include("apps.main.urls")),
]

# Static and media files serving in development mode
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
