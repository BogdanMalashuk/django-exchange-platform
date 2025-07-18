from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ads.urls')),
    path('auth/', include('authorization.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]
