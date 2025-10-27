from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from .filters import WorkspaceFilterClass

from .models import Workspace
from .serializers import WorkspaceSerializer

from django.shortcuts import render

class WorkspaceViewSet(viewsets.ModelViewSet):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer
    permission_classes = [ IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = WorkspaceFilterClass

    #""" IsAdminUser """ 