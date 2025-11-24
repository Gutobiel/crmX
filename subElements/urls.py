from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ContratosSubelementViewSet, SubElementViewSet

router = DefaultRouter()
router.register('subElement', SubElementViewSet)
router.register('contratos-subelements', ContratosSubelementViewSet, basename='contratos-subelements')

urlpatterns = [
    path('', include(router.urls)),
   
]