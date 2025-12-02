from rest_framework import viewsets
<<<<<<< HEAD
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from .filters import SubElementFilterClass

from .models import SubElement, ContratosSubelement
from .serializers import SubElementSerializer, ContratosSubelementSerializer

from django.shortcuts import render
=======
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from .filters import SubElementFilterClass

from .models import ContratosSubelement, SubElement
from .serializers import ContratosSubelementSerializer, SubElementSerializer
>>>>>>> 097a7b36037ca8e7c5fa6d1fab43538e5c3c1a4b

class SubElementViewSet(viewsets.ModelViewSet):
    queryset = SubElement.objects.all()
    serializer_class = SubElementSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = SubElementFilterClass

    #""" IsAdminUser """ 


class ContratosSubelementViewSet(viewsets.ModelViewSet):
<<<<<<< HEAD
    queryset = ContratosSubelement.objects.all()
=======
    queryset = ContratosSubelement.objects.select_related('element')
>>>>>>> 097a7b36037ca8e7c5fa6d1fab43538e5c3c1a4b
    serializer_class = ContratosSubelementSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        element_id = self.request.query_params.get('element')
<<<<<<< HEAD
        if element_id:
            queryset = queryset.filter(element_id=element_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save()
=======
        sheet_id = self.request.query_params.get('sheet')
        if element_id:
            queryset = queryset.filter(element_id=element_id)
        if sheet_id:
            queryset = queryset.filter(element__sheet_id=sheet_id)
        return queryset

    def perform_create(self, serializer):
        # Exige que o subelemento esteja vinculado a um elemento de contratos
        element_id = self.request.data.get('element')
        if not element_id:
            raise ValidationError({'element': 'Este campo é obrigatório.'})
        serializer.save()
>>>>>>> 097a7b36037ca8e7c5fa6d1fab43538e5c3c1a4b
