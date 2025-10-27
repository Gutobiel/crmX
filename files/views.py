from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from .filters import FileFilterClass

from .models import File
from .serializers import FileSerializer

from django.shortcuts import render

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [ IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = FileFilterClass

    #""" IsAdminUser """ 