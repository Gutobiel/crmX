from django.contrib import admin
from .models import Sheet, Column, Row, Cell


class ColumnInline(admin.TabularInline):
    model = Column
    extra = 0
    fields = ['nome', 'order', 'editavel']
    ordering = ['order']


class CellInline(admin.TabularInline):
    model = Cell
    extra = 0
    fields = ['column', 'value']


@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = ['nome', 'board', 'tipo', 'created_at', 'updated_at']
    list_filter = ['tipo', 'board', 'created_at']
    search_fields = ['nome', 'board__nome']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [ColumnInline]
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('board', 'nome', 'tipo')
        }),
        ('Configuração Legada (deprecated)', {
            'fields': ('colunas', 'linhas'),
            'classes': ('collapse',)
        }),
        ('Anotações', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = ['nome', 'sheet', 'order', 'editavel']
    list_filter = ['sheet', 'editavel']
    search_fields = ['nome', 'sheet__nome']
    ordering = ['sheet', 'order']


@admin.register(Row)
class RowAdmin(admin.ModelAdmin):
    list_display = ['id', 'sheet', 'parent', 'order', 'is_subrow']
    list_filter = ['sheet', 'is_subrow']
    search_fields = ['sheet__nome']
    ordering = ['sheet', 'order']
    inlines = [CellInline]


@admin.register(Cell)
class CellAdmin(admin.ModelAdmin):
    list_display = ['id', 'row', 'column', 'value']
    list_filter = ['row__sheet', 'column']
    search_fields = ['value', 'row__sheet__nome', 'column__nome']
