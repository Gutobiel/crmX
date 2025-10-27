from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from .filters import ElementFilterClass

from .models import Element
from .serializers import ElementSerializer

from django.shortcuts import render

class ElementViewSet(viewsets.ModelViewSet):
    queryset = Element.objects.all()
    serializer_class = ElementSerializer
    permission_classes = [ IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = ElementFilterClass

    #IsAdminUser 