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
<<<<<<< HEAD
    
=======

>>>>>>> 097a7b36037ca8e7c5fa6d1fab43538e5c3c1a4b
    class Meta:
        model = ContratosSubelement
        fields = '__all__'
        read_only_fields = (
            'valor_total',
            'valor_unitario_reajustado',
            'valor_total_reajustado',
        )