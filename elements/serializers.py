from rest_framework import serializers
from .models import Element, ElementFreelancer, ElementCollaborator, ContratosElement

class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = '__all__'

