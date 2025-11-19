from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SubElementViewSet, ContratosSubelementViewSet

router = DefaultRouter()
router.register('subElement', SubElementViewSet)
router.register('contratos-subelements', ContratosSubelementViewSet)

urlpatterns = [
    path('', include(router.urls)),
   
]