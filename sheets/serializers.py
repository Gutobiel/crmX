from rest_framework import serializers
from .models import Sheet


class SheetSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    colunas = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Sheet
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']