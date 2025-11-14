from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView)

urlpatterns = [
    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/v1/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('api/v1/', include('authentication.urls')),
    path('api/v1/', include('boards.urls')),
    path('api/v1/', include('elements.urls')),
    path('api/v1/', include('files.urls')),
    path('api/v1/', include('products.urls')),
    path('api/v1/', include('sheets.urls')),
    path('api/v1/', include('subElements.urls')),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('workspaces.urls')),
    path('admin/', admin.site.urls),
    path('', include('frontend.urls')),
]