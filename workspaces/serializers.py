from rest_framework import serializers
from .models import Workspace, WorkspaceMember
from django.contrib.auth import get_user_model

User = get_user_model()

class MemberSerializer(serializers.ModelSerializer):
    """Serializer para exibir informações básicas do membro"""
    name = serializers.SerializerMethodField()
    initials = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'name', 'initials']
    
    def get_name(self, obj):
        if hasattr(obj, 'profile'):
            full_name = f"{obj.profile.First_name} {obj.profile.last_name}".strip()
            if full_name and full_name != "Não informado Não informado":
                return full_name
        return obj.get_full_name() or obj.username
    
    def get_initials(self, obj):
        if hasattr(obj, 'profile'):
            first = obj.profile.First_name if obj.profile.First_name != "Não informado" else ""
            last = obj.profile.last_name if obj.profile.last_name != "Não informado" else ""
            if first and last:
                return f"{first[0]}{last[0]}".upper()
            elif first:
                return first[0:2].upper()
        
        # Fallback para username
        if obj.get_full_name():
            parts = obj.get_full_name().split()
            if len(parts) >= 2:
                return f"{parts[0][0]}{parts[-1][0]}".upper()
        return obj.username[0:2].upper()

class WorkspaceSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    members = serializers.SerializerMethodField()
    folders_count = serializers.SerializerMethodField()
    is_owner = serializers.SerializerMethodField()
    
    class Meta:
        model = Workspace
        fields = '__all__'
    
    def get_members_count(self, obj):
        # Conta o dono + membros compartilhados
        return obj.workspace_members.count() + 1 if obj.dono else obj.workspace_members.count()
    
    def get_members(self, obj):
        # Lista com o dono primeiro, depois os membros
        members = []
        if obj.dono:
            members.append(MemberSerializer(obj.dono).data)
        
        # Adiciona os outros membros
        workspace_members = obj.workspace_members.select_related('user').all()
        for wm in workspace_members:
            members.append(MemberSerializer(wm.user).data)
        
        return members
    
    def get_folders_count(self, obj):
        return obj.boards.count()
    
    def get_is_owner(self, obj):
        request = self.context.get('request')
        if request and request.user:
            return obj.dono == request.user
        return False

class AddMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    board_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        allow_empty=False
    )