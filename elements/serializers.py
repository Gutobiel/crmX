from rest_framework import serializers
from .models import Element, ElementCollaborator, ContratosElement, ProductElement

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'


class ContratosElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratosElement
        fields = '__all__'


class ElementCollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementCollaborator
        fields = '__all__'


class ProductElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductElement
        fields = '__all__'

