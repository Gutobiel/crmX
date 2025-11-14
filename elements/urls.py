from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    ElementViewSet,
    ContratosElementViewSet,
    ElementCollaboratorViewSet,
    ProductElementViewSet
)

router = DefaultRouter()
router.register('element', ElementViewSet)
router.register('contratos', ContratosElementViewSet)
router.register('collaborators', ElementCollaboratorViewSet)
router.register('products', ProductElementViewSet)

urlpatterns = [
    path('', include(router.urls)),
   
]