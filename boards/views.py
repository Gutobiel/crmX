from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .filters import BoardFilterClass
from .models import Board
from .serializers import BoardSerializer, BoardDetailSerializer  # importa os dois
from django.shortcuts import render

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = BoardFilterClass

    def get_serializer_class(self):
        """
        Usa o serializer detalhado quando for uma ação 'retrieve' (GET /api/boards/{id}/),
        e o simples para listagem e demais ações.
        """
        if self.action == 'retrieve':
            return BoardDetailSerializer
        return BoardSerializer
