from django.db import models
from django.contrib.auth.models import User
from mixins.models import TimestampMixin, ActiveMixin

class Workspace(TimestampMixin, ActiveMixin, models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nome da Área de Trabalho'
    )
    dono = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='owned_workspaces',
        verbose_name='Dono'
    )
    membros = models.ManyToManyField(
        User,
        through='WorkspaceMember',
        related_name='shared_workspaces',
        blank=True,
        verbose_name='Membros'
    )

    class Meta:
        verbose_name = 'Área de Trabalho'
        verbose_name_plural = 'Áreas de Trabalho'

    def __str__(self):
        return self.nome


class WorkspaceMember(TimestampMixin, models.Model):
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
        'boards.Board',
        blank=True,
        related_name='member_access',
        verbose_name='Pastas com Acesso'
    )

    class Meta:
        verbose_name = 'Membro do Workspace'
        verbose_name_plural = 'Membros dos Workspaces'
        unique_together = ('workspace', 'user')

    def __str__(self):
        return f"{self.user.username} em {self.workspace.nome}"
