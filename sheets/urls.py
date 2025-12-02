from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SheetViewSet

router = DefaultRouter()
router.register('sheet', SheetViewSet)

urlpatterns = [
    path('', include(router.urls)),
   
]