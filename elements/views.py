from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from .filters import ElementFilterClass

from .models import Element, ContratosElement, ElementCollaborator, ProductElement
from .serializers import (
    ElementSerializer, 
    ContratosElementSerializer,
    ElementCollaboratorSerializer,
    ProductElementSerializer
)

from django.shortcuts import render

class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    permission_classes = [ IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = ElementFilterClass


class ContratosElementViewSet(viewsets.ModelViewSet):
    queryset = ContratosElement.objects.all()
    serializer_class = ContratosElementSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sheet_id = self.request.query_params.get('sheet', None)
        if sheet_id:
            queryset = queryset.filter(sheet_id=sheet_id)
        return queryset
    
    def perform_create(self, serializer):
        # Se sheet for fornecido, usar ele; senão usar board (retrocompatibilidade)
        if 'sheet' in self.request.data and not self.request.data.get('board'):
            serializer.save()
        else:
            serializer.save()


class ElementCollaboratorViewSet(viewsets.ModelViewSet):
    queryset = ElementCollaborator.objects.all()
    serializer_class = ElementCollaboratorSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sheet_id = self.request.query_params.get('sheet', None)
        if sheet_id:
            queryset = queryset.filter(sheet_id=sheet_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save()


class ProductElementViewSet(viewsets.ModelViewSet):
    queryset = ProductElement.objects.all()
    serializer_class = ProductElementSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        sheet_id = self.request.query_params.get('sheet', None)
        if sheet_id:
            queryset = queryset.filter(sheet_id=sheet_id)
        return queryset
    
    def perform_create(self, serializer):
        serializer.save()

    #IsAdminUser 