from rest_framework import serializers
from .models import SubElement, ContratosSubelement

class SubElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubElement
        fields = '__all__'

class ContratosSubelementSerializer(serializers.ModelSerializer):
    valor_total = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    valor_unitario_reajustado = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    valor_total_reajustado = serializers.DecimalField(max_digits=15, decimal_places=2, required=False)
    
    class Meta:
        model = ContratosSubelement
        fields = '__all__'