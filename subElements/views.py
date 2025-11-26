from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated
from .filters import SubElementFilterClass

from .models import ContratosSubelement, SubElement
from .serializers import ContratosSubelementSerializer, SubElementSerializer

class SubElementViewSet(viewsets.ModelViewSet):
    queryset = SubElement.objects.all()
    serializer_class = SubElementSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = SubElementFilterClass

    #""" IsAdminUser """ 


class ContratosSubelementViewSet(viewsets.ModelViewSet):
    queryset = ContratosSubelement.objects.select_related('element')
    serializer_class = ContratosSubelementSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get_queryset(self):
        queryset = super().get_queryset()
        element_id = self.request.query_params.get('element')
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
