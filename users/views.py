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
    permission_classes = [ IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = UserFilterClass

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get('q', '').strip()
        
        if len(query) < 2:
            return Response([], status=status.HTTP_200_OK)
        
        # Search by username, email, or profile name
        users = User.objects.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(profile__nome__icontains=query)
        ).select_related('profile').distinct()[:10]
        
        results = []
        for user in users:
            results.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'nome': user.profile.nome if hasattr(user, 'profile') else None
            })
        
        return Response(results, status=status.HTTP_200_OK)

    #""" IsAdminUser """ 