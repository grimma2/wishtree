from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static

from letters.views import index


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('letters/', include('letters.urls')),
    path('usertools/', include('usertools.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
