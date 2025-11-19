from rest_framework import serializers
from .models import SubElement, ContratosSubelement

class SubElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubElement
        fields = '__all__'


class ContratosSubelementSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratosSubelement
        fields = '__all__'
        read_only_fields = (
            'valor_total',
            'valor_unitario_reajustado',
            'valor_total_reajustado',
        )