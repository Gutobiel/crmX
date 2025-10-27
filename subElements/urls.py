from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SubElementViewSet

router = DefaultRouter()
router.register('subElement', SubElementViewSet)

urlpatterns = [
    path('', include(router.urls)),
   
]