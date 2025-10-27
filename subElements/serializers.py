from rest_framework import serializers
from .models import SubElement

class SubElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubElement
        fields = '__all__'