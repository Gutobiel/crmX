from rest_framework import serializers
from .models import Sheet


class SheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sheet
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']