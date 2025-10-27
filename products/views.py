from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser, DjangoModelPermissions, IsAuthenticated
from .filters import ProductFilterClass

from .models import Product
from .serializers import ProductSerializer

from django.shortcuts import render

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ IsAuthenticated, DjangoModelPermissions]
    rql_filter_class = ProductFilterClass

    #""" IsAdminUser """ 