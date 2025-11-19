from rest_framework import viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from .filters import SubElementFilterClass

from .models import SubElement, ContratosSubelement
from .serializers import SubElementSerializer, ContratosSubelementSerializer

from django.shortcuts import render

class SubElementViewSet(viewsets.ModelViewSet):
    queryset = SubElement.objects.all()
    serializer_class = SubElementSerializer
    permission_classes = [ IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = SubElementFilterClass

    #""" IsAdminUser """ 


class ContratosSubelementViewSet(viewsets.ModelViewSet):
    queryset = ContratosSubelement.objects.all()
    serializer_class = ContratosSubelementSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        element_id = self.request.query_params.get('element')
        if element_id:
            queryset = queryset.filter(element_id=element_id)
        return queryset

    def perform_create(self, serializer):
        serializer.save()