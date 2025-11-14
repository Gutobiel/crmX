from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SheetViewSet, RowViewSet, ColumnViewSet, CellViewSet

router = DefaultRouter()
router.register('sheet', SheetViewSet)
router.register('row', RowViewSet)
router.register('column', ColumnViewSet)
router.register('cell', CellViewSet)

urlpatterns = [
    path('', include(router.urls)),
   
]