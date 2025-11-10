from django.contrib import admin
from .models import Sheet

@admin.register(Sheet)
class SheetAdmin(admin.ModelAdmin):
    list_display = ['nome', 'board', 'tipo', 'created_at', 'updated_at']
    list_filter = ['tipo', 'board', 'created_at']
    search_fields = ['nome', 'board__nome']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('board', 'nome', 'tipo')
        }),
        ('Configuração', {
            'fields': ('colunas', 'linhas'),
            'classes': ('collapse',)
        }),
        ('Anotações', {
            'fields': ('anotacao',),
            'classes': ('collapse',)
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
