from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from .filters import SheetFilterClass

from .models import Sheet
from .serializers import SheetSerializer

from django.shortcuts import render

class SheetViewSet(viewsets.ModelViewSet):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = [ IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = SheetFilterClass

    @action(detail=False, methods=['get'])
    def templates(self, request):
        """Retorna os modelos de planilha disponíveis"""
        templates = [
            {
                'id': 'generico',
                'nome': 'Genérico',
                'descricao': 'Planilha totalmente personalizável',
                'icon': 'fa-table',
                'colunas': []
            },
            {
                'id': 'contratos',
                'nome': 'Contratos',
                'descricao': 'Modelo para gestão de contratos',
                'icon': 'fa-file-contract',
                'colunas': [
                    {'nome': 'Elemento', 'editavel': False},
                    {'nome': 'Empresa', 'editavel': False},
                    {'nome': 'Objeto', 'editavel': False},
                    {'nome': 'Qtd Total Itens', 'editavel': False},
                    {'nome': 'Valor Total Anterior', 'editavel': False},
                    {'nome': 'Valor Total Reajustado', 'editavel': False}
                ]
            },
            {
                'id': 'colaboradores',
                'nome': 'Colaboradores',
                'descricao': 'Modelo para gestão de pessoas',
                'icon': 'fa-users',
                'colunas': [
                    {'nome': 'Nome', 'editavel': False},
                    {'nome': 'Cargo', 'editavel': False},
                    {'nome': 'Salário Bruto', 'editavel': False},
                    {'nome': 'Benefício Alimentação', 'editavel': False},
                    {'nome': 'Benefício Transporte', 'editavel': False}
                ]
            },
            {
                'id': 'produtos',
                'nome': 'Produtos',
                'descricao': 'Modelo para catálogo de produtos',
                'icon': 'fa-box',
                'colunas': [
                    {'nome': 'Código', 'editavel': False},
                    {'nome': 'Nome', 'editavel': False},
                    {'nome': 'Categoria', 'editavel': False},
                    {'nome': 'Preço', 'editavel': False},
                    {'nome': 'Estoque', 'editavel': False}
                ]
            }
        ]
        return Response(templates)

    #""" IsAdminUser """ 