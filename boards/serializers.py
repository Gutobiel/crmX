from rest_framework import serializers
from .models import Board
from sheets.serializers import SheetSerializer

class BoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = '__all__'

class BoardDetailSerializer(serializers.ModelSerializer):
    """Serializer completo com aninhamentos"""
    sheets = SheetSerializer(many=True, read_only=True)

    class Meta:
        model = Board
        fields = '__all__'