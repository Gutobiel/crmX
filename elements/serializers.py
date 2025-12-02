from rest_framework import serializers
from .models import Element, ElementCollaborator, ContratosElement, ProductElement
from subElements.serializers import ContratosSubelementSerializer

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'


class ContratosElementSerializer(serializers.ModelSerializer):
    subelements = ContratosSubelementSerializer(source='subElements', many=True, read_only=True)

    class Meta:
        model = ContratosElement
        fields = '__all__'
        read_only_fields = ['qtd_total_itens', 'valor_total_anterior', 'valor_total_reajustado']


class ElementCollaboratorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElementCollaborator
        fields = '__all__'


class ProductElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductElement
        fields = '__all__'

