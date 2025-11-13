from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .filters import SheetFilterClass

from .models import Sheet, Column, Row, Cell
from .serializers import SheetSerializer, RowSerializer, ColumnSerializer, CellSerializer
from boards.models import Board

from django.shortcuts import render
from django.db import transaction

class SheetViewSet(viewsets.ModelViewSet):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = SheetFilterClass

    def get_queryset(self):
        queryset = super().get_queryset().select_related('board', 'board__workspace')
        board_id = self.request.query_params.get("board")
        if board_id:
            queryset = queryset.filter(board_id=board_id)
        return queryset.prefetch_related(
            'columns',
            'rows__cells__column',
            'rows__subrows__cells__column',
            'contratos_elements__subElements'
        )

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

    # --- Nova estrutura relacional: endpoints para manipulação ---
    @action(detail=True, methods=['post'])
    def add_row(self, request, pk=None):
        """Adiciona uma linha principal vazia à planilha"""
        sheet = self.get_object()
        
        with transaction.atomic():
            # Determinar a ordem da nova linha
            max_order = Row.objects.filter(sheet=sheet, is_subrow=False).count()
            
            # Criar linha principal
            row = Row.objects.create(
                sheet=sheet,
                order=max_order,
                is_subrow=False
            )
            
            # Criar células vazias para todas as colunas
            columns = sheet.columns.all()
            for column in columns:
                Cell.objects.create(
                    row=row,
                    column=column,
                    value=''
                )
        
        return Response({'status': 'ok', 'row_id': row.id})

    @action(detail=True, methods=['post'])
    def add_subrow(self, request, pk=None):
        """Adiciona uma sub-linha a uma linha principal. Body: {"parent_row_id": 123}"""
        sheet = self.get_object()
        parent_row_id = request.data.get('parent_row_id')
        
        if not parent_row_id:
            return Response({'error': 'parent_row_id é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            parent_row = Row.objects.get(id=parent_row_id, sheet=sheet)
        except Row.DoesNotExist:
            return Response({'error': 'Linha pai não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        
        with transaction.atomic():
            # Determinar a ordem da sub-linha
            max_order = Row.objects.filter(sheet=sheet, parent=parent_row).count()
            
            # Criar sub-linha
            subrow = Row.objects.create(
                sheet=sheet,
                parent=parent_row,
                order=max_order,
                is_subrow=True
            )
            
            # Criar células vazias
            columns = sheet.columns.all()
            for column in columns:
                Cell.objects.create(
                    row=subrow,
                    column=column,
                    value=''
                )
        
        return Response({'status': 'ok', 'row_id': subrow.id})

    @action(detail=True, methods=['delete'])
    def remove_row(self, request, pk=None):
        """Remove uma linha (e suas sub-linhas se for linha principal). Body: {"row_id": 123}"""
        sheet = self.get_object()
        row_id = request.data.get('row_id')
        
        if not row_id:
            return Response({'error': 'row_id é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            row = Row.objects.get(id=row_id, sheet=sheet)
            row.delete()  # CASCADE deleta células e sub-linhas
            return Response({'status': 'ok'})
        except Row.DoesNotExist:
            return Response({'error': 'Linha não encontrada'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def add_column(self, request, pk=None):
        """Adiciona uma nova coluna (apenas para tipo generico). Body: {"nome": "Nova Coluna"}"""
        sheet = self.get_object()
        
        if sheet.tipo != 'generico':
            return Response({'error': 'Só permitido em planilha genérica'}, status=status.HTTP_400_BAD_REQUEST)
        
        nome = request.data.get('nome')
        if not nome:
            return Response({'error': 'Nome é obrigatório'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Verificar duplicados
        if sheet.columns.filter(nome=nome).exists():
            return Response({'error': 'Coluna já existe'}, status=status.HTTP_400_BAD_REQUEST)
        
        with transaction.atomic():
            # Determinar ordem
            max_order = sheet.columns.count()
            
            # Criar coluna
            column = Column.objects.create(
                sheet=sheet,
                nome=nome,
                order=max_order,
                editavel=True
            )
            
            # Criar células vazias para todas as linhas existentes
            rows = sheet.rows.all()
            for row in rows:
                Cell.objects.create(
                    row=row,
                    column=column,
                    value=''
                )
        
        return Response({'status': 'ok', 'column_id': column.id})

    @action(detail=True, methods=['patch'])
    def update_column(self, request, pk=None):
        """Atualiza nome de uma coluna. Body: {"column_id": 123, "nome": "Novo Nome"}"""
        sheet = self.get_object()
        column_id = request.data.get('column_id')
        nome = request.data.get('nome')
        
        if not column_id or not nome:
            return Response({'error': 'column_id e nome são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            column = Column.objects.get(id=column_id, sheet=sheet)
            column.nome = nome
            column.save(update_fields=['nome'])
            return Response({'status': 'ok'})
        except Column.DoesNotExist:
            return Response({'error': 'Coluna não encontrada'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def update_cell(self, request, pk=None):
        """Atualiza ou cria uma célula. Body: {"row_id": 123, "column_id": 456, "value": "ABC", "cell_id": 789}"""
        sheet = self.get_object()
        row_id = request.data.get('row_id')
        column_id = request.data.get('column_id')
        value = request.data.get('value', '')
        cell_id = request.data.get('cell_id')
        
        if not row_id or not column_id:
            return Response({'error': 'row_id e column_id são obrigatórios'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            row = Row.objects.get(id=row_id, sheet=sheet)
            column = Column.objects.get(id=column_id, sheet=sheet)
            
            # Atualizar ou criar célula
            cell, created = Cell.objects.update_or_create(
                row=row,
                column=column,
                defaults={'value': value}
            )
            
            return Response({'status': 'ok', 'cell_id': cell.id, 'created': created})
        except Row.DoesNotExist:
            return Response({'error': 'Linha não encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Column.DoesNotExist:
            return Response({'error': 'Coluna não encontrada'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'], url_path='nested')
    def nested(self, request, pk=None):
        """Retorna a planilha com dados aninhados de board, workspace e elementos relacionados."""
        sheet = self.get_object()
        serializer = self.get_serializer(sheet)

        board = sheet.board
        workspace = board.workspace if board else None

        board_data = None
        if board:
            board_data = {
                'id': board.id,
                'nome': board.nome,
                'workspace': board.workspace_id,
                'created_at': board.created_at.isoformat() if hasattr(board, 'created_at') and board.created_at else None,
                'updated_at': board.updated_at.isoformat() if hasattr(board, 'updated_at') and board.updated_at else None,
            }

        workspace_data = None
        if workspace:
            workspace_data = {
                'id': workspace.id,
                'nome': workspace.nome,
            }

        return Response({
            'sheet': serializer.data,
            'board': board_data,
            'workspace': workspace_data,
        })



class CellViewSet(viewsets.ModelViewSet):
    queryset = Cell.objects.all()
    serializer_class = CellSerializer

class ColumnViewSet(viewsets.ModelViewSet):
    queryset = Column.objects.all()
    serializer_class = ColumnSerializer

class RowViewSet(viewsets.ModelViewSet):
    queryset = Row.objects.all()
    serializer_class = RowSerializer
    #""" IsAdminUser """ 