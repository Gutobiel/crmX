from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
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
        # Exige sempre o campo 'sheet' para criação de contratos
        sheet_id = self.request.data.get('sheet')
        if not sheet_id:
            raise ValidationError({'sheet': 'Este campo é obrigatório para contratos.'})
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