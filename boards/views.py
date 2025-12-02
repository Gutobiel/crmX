from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from .filters import BoardFilterClass
from .models import Board
from .serializers import BoardSerializer
from django.shortcuts import render

class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = BoardFilterClass

    def get_serializer_class(self):

        if self.action == 'retrieve':
            return BoardSerializer
        return BoardSerializer
