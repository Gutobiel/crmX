from django.urls import path, include
from rest_framework.routers import DefaultRouter

<<<<<<< HEAD
from .views import SubElementViewSet, ContratosSubelementViewSet

router = DefaultRouter()
router.register('subElement', SubElementViewSet)
router.register('contratos-subelements', ContratosSubelementViewSet)
=======
from .views import ContratosSubelementViewSet, SubElementViewSet

router = DefaultRouter()
router.register('subElement', SubElementViewSet)
router.register('contratos-subelements', ContratosSubelementViewSet, basename='contratos-subelements')
>>>>>>> 097a7b36037ca8e7c5fa6d1fab43538e5c3c1a4b

urlpatterns = [
    path('', include(router.urls)),
   
]