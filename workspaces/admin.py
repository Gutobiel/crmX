from django.contrib import admin
from .models import Workspace

class WorkspaceInline(admin.TabularInline):
    model = Workspace   
    extra = 1  # mostra 1 campo vazio para adicionar
    fields = ('nome')

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('nome', 'ativo','created_at', 'updated_at')
    search_fields = ('nome', 'created_at')
    list_filter = ('nome', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 5
    list_editable = ("ativo",)


    