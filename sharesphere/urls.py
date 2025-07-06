from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from ridemate import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('login.urls')),  # Ensure 'login' app is registered
    path('buysell/', include('BuySell.urls')),
    path('ridemate/', include('ridemate.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # Ensure static files are served