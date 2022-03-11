from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('license_checker.urls'))
]

urlpatterns.extend(
    static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))

urlpatterns.extend(
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
