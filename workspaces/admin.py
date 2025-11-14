from django.contrib import admin
from .models import Workspace, WorkspaceMember

class WorkspaceInline(admin.TabularInline):
    model = Workspace   
    extra = 1  # mostra 1 campo vazio para adicionar
    fields = ('nome')

class WorkspaceMemberInline(admin.TabularInline):
    model = WorkspaceMember
    extra = 0
    fields = ('user', 'accessible_boards')
    filter_horizontal = ('accessible_boards',)

@admin.register(Workspace)
class WorkspaceAdmin(admin.ModelAdmin):
    list_display = ('nome', 'dono', 'ativo','created_at', 'updated_at')
    search_fields = ('nome', 'created_at')
    list_filter = ('nome', 'created_at')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    list_per_page = 5
    list_editable = ("ativo",)
    inlines = [WorkspaceMemberInline]

@admin.register(WorkspaceMember)
class WorkspaceMemberAdmin(admin.ModelAdmin):
    list_display = ('workspace', 'user', 'created_at')
    list_filter = ('workspace', 'created_at')
    search_fields = ('workspace__nome', 'user__username', 'user__email')
    filter_horizontal = ('accessible_boards',)
    ordering = ('-created_at',)


    