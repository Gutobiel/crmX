from django.db import models
from workspaces.models import Workspace
from mixins.models import TimestampMixin

class Board(TimestampMixin, models.Model):
    workspace = models.ForeignKey(
        Workspace,
        on_delete=models.CASCADE,
        related_name='boards',
        verbose_name='Área de Trabalho'
    )
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Quadro'
    )

    class Meta:
        verbose_name = 'Quadro'
        verbose_name_plural = 'Quadros'

    def __str__(self):
        return f"{self.workspace.nome} - {self.nome}"
