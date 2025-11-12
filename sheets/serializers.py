from rest_framework import serializers
from .models import Sheet, Column, Row, Cell


class CellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cell
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class ColumnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Column
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class RowSerializer(serializers.ModelSerializer):
    cells = CellSerializer(many=True, read_only=True)
    
    class Meta:
        model = Row
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']


class SheetSerializer(serializers.ModelSerializer):
    tipo_display = serializers.CharField(source='get_tipo_display', read_only=True)
    colunas = serializers.ListField(
        child=serializers.DictField(),
        write_only=True,
        required=False
    )
    columns = ColumnSerializer(many=True, read_only=True)  # ← Para leitura
    rows = RowSerializer(many=True, read_only=True)
    
    class Meta:
        model = Sheet
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        print(f"🔹 SheetSerializer.create() - Colunas recebidas: {validated_data.get('colunas', [])}")
        
        colunas_data = validated_data.pop('colunas', [])
        
        # Criar Sheet
        sheet = Sheet.objects.create(**validated_data)
        print(f"✅ Sheet criada: ID={sheet.id}, Nome={sheet.nome}")
        
        # Criar Columns
        for idx, col_data in enumerate(colunas_data):
            column = Column.objects.create(
                sheet=sheet,
                nome=col_data['nome'],
                order=idx,
                editavel=col_data.get('editavel', True)
            )
            print(f"  ✓ Coluna criada: {column.nome} (order={column.order})")
        
        # ⭐ IMPORTANTE: Recarregar o objeto com as colunas
        sheet.refresh_from_db()
        
        return sheet
    
    def to_representation(self, instance):
        """Garante que as colunas sejam incluídas na resposta"""
        ret = super().to_representation(instance)
        
        # Force o carregamento das colunas
        ret['columns'] = ColumnSerializer(instance.columns.all(), many=True).data
        ret['rows'] = RowSerializer(instance.rows.all(), many=True).data
        
        return ret