from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from .filters import WorkspaceFilterClass

from .models import Workspace, WorkspaceMember
from .serializers import WorkspaceSerializer, AddMemberSerializer
from boards.models import Board
from django.contrib.auth import get_user_model

from django.shortcuts import render

User = get_user_model()

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [ IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = WorkspaceFilterClass

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

    def perform_create(self, serializer):
        # Define o dono como o usuário autenticado ao criar
        serializer.save(dono=self.request.user)

    @action(detail=True, methods=['post'], url_path='add-member')
    def add_member(self, request, pk=None):
        workspace = self.get_object()
        
        # Check if user is owner
        if workspace.dono != request.user:
            return Response(
                {'detail': 'Apenas o dono pode adicionar membros'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = AddMemberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user_id = serializer.validated_data['user_id']
        board_ids = serializer.validated_data['board_ids']
        
        # Get user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Usuário não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user is already a member
        if WorkspaceMember.objects.filter(workspace=workspace, user=user).exists():
            return Response(
                {'detail': 'Usuário já é membro deste workspace'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate boards belong to this workspace
        boards = Board.objects.filter(id__in=board_ids, workspace=workspace)
        if boards.count() != len(board_ids):
            return Response(
                {'detail': 'Algumas pastas não pertencem a este workspace'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create workspace member
        member = WorkspaceMember.objects.create(workspace=workspace, user=user)
        member.accessible_boards.set(boards)
        
        return Response(
            {'detail': 'Membro adicionado com sucesso'},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['post'], url_path='remove-member')
    def remove_member(self, request, pk=None):
        workspace = self.get_object()
        
        # Check if user is owner
        if workspace.dono != request.user:
            return Response(
                {'detail': 'Apenas o dono pode remover membros'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        user_id = request.data.get('user_id')
        if not user_id:
            return Response(
                {'detail': 'user_id é obrigatório'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get user
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response(
                {'detail': 'Usuário não encontrado'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if user is the owner
        if workspace.dono == user:
            return Response(
                {'detail': 'Não é possível remover o proprietário'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user is a member
        try:
            member = WorkspaceMember.objects.get(workspace=workspace, user=user)
            member.delete()
            return Response(
                {'detail': 'Membro removido com sucesso'},
                status=status.HTTP_200_OK
            )
        except WorkspaceMember.DoesNotExist:
            return Response(
                {'detail': 'Usuário não é membro deste workspace'},
                status=status.HTTP_404_NOT_FOUND
            )
