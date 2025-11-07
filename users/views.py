from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from .filters import UserFilterClass

from .models import Profile, UserRole, Role
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.db.models import Q

from django.shortcuts import render

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = UserFilterClass

    def get_permissions(self):
        """Permite que ação de busca seja acessível a qualquer usuário autenticado,
        sem necessidade de permissões de modelo (view_user)."""
        if getattr(self, 'action', None) == 'search':
            return [IsAuthenticated()]
        return super().get_permissions()

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get('q', '').strip()
        
        if len(query) < 2:
            return Response([], status=status.HTTP_200_OK)
        
        # Search by username, email, or profile name
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(profile__First_name__icontains=query) |
            Q(profile__last_name__icontains=query)
        ).select_related('profile').order_by('username').distinct()[:10]
        
        results = []
        for user in users:
            # Monta nome legível priorizando profile, depois get_full_name, depois username
            nome = None
            if hasattr(user, 'profile') and user.profile:
                fn = user.profile.First_name if user.profile.First_name != 'Não informado' else ''
                ln = user.profile.last_name if user.profile.last_name != 'Não informado' else ''
                full_name = f"{fn} {ln}".strip()
                if full_name:
                    nome = full_name
            if not nome:
                nome = user.get_full_name() or user.username

            results.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'nome': nome,
                'has_profile': hasattr(user, 'profile') and user.profile is not None
            })
        
        return Response(results, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='quick-list')
    def quick_list(self, request):
        """Retorna até 10 usuários para depuração rápida da busca"""
        users = User.objects.all().order_by('id')[:10]
        data = [
            {
                'id': u.id,
                'username': u.username,
                'email': u.email,
                'has_profile': hasattr(u, 'profile'),
            } for u in users
        ]
        return Response(data, status=status.HTTP_200_OK)

    #""" IsAdminUser """ 