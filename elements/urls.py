from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ElementViewSet

router = DefaultRouter()
router.register('element', ElementViewSet)

urlpatterns = [
    path('', include(router.urls)),
   
]