from django.db import models
from django.contrib.auth.models import User
from workspaces.models import Workspace
from boards.models import Board


class WorkspaceMember(models.Model):
    """
    Controla acesso de membros às áreas de trabalho e boards específicos.
    """
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='workspace_members',
        verbose_name='Área de Trabalho'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='workspace_memberships',
        verbose_name='Usuário'
    )
    accessible_boards = models.ManyToManyField(
        Board,
        blank=True,
        related_name='member_access',
        verbose_name='Pastas com Acesso'
    )
    added_at = models.DateTimeField(auto_now_add=True, verbose_name='Adicionado em')

    class Meta:
        verbose_name = 'Membro do Workspace'
        verbose_name_plural = 'Membros dos Workspaces'
        unique_together = ('workspace', 'user')

    def __str__(self):
        return f"{self.user.username} em {self.workspace.nome}"
