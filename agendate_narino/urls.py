"""
URL configuration for agendate_narino project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from eventos import views as eventos_views

urlpatterns = [
    path('', eventos_views.home, name='home'),
    path('admin/', admin.site.urls),
    path('usuarios/', include('usuarios.urls')),
    path('events/', include('eventos.urls')),
    path('events/explore/', eventos_views.evento_explore, name='evento_explore'),
    path('messaging/', include('messaging.urls')),
    path('core/', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
