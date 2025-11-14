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