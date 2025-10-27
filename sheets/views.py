from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from .filters import SheetFilterClass

from .models import Sheet
from .serializers import SheetSerializer

from django.shortcuts import render

class SheetViewSet(viewsets.ModelViewSet):
    queryset = Sheet.objects.all()
    serializer_class = SheetSerializer
    permission_classes = [ IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = SheetFilterClass

    #""" IsAdminUser """ 