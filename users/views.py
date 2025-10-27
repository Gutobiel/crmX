from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from .filters import UserFilterClass

from .models import Profile, UserRole, Role
from django.contrib.auth.models import User
from .serializers import UserSerializer

from django.shortcuts import render

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [ IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = UserFilterClass

    #""" IsAdminUser """ 