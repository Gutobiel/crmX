from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from .filters import SheetFilterClass

from .models import Sheet
from .serializers import SheetSerializer
from boards.models import Board

class SheetViewSet(viewsets.ModelViewSet):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = SheetFilterClass

    def get_queryset(self):
        queryset = super().get_queryset()
        board_id = self.request.query_params.get("board")
        if board_id:
            queryset = queryset.filter(board_id=board_id)
        return queryset.prefetch_related('columns', 'rows')