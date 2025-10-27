from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from .filters import SubElementFilterClass

from .models import SubElement
from .serializers import SubElementSerializer

from django.shortcuts import render

class SubElementViewSet(viewsets.ModelViewSet):
    queryset = SubElement.objects.all()
    serializer_class = SubElementSerializer
    permission_classes = [ IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = SubElementFilterClass

    #""" IsAdminUser """ 