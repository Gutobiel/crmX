from django.db import models
from boards.models import Board
from mixins.models import TimestampMixin, NotesMixin

class Sheet(NotesMixin, TimestampMixin, models.Model):
    TIPO_CHOICES = [
        ('generico', 'Genérico'),
        ('contratos', 'Contratos'),
        ('colaboradores', 'Colaboradores'),
        ('produtos', 'Produtos'),
    ]
    
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name='sheets',
        verbose_name='Quadro'
    )
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome da Planilha'
    )
    tipo = models.CharField(
        max_length=20,
        choices=TIPO_CHOICES,
        default='generico',
        verbose_name='Tipo de Planilha'
    )
    colunas = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Configuração das Colunas',
        help_text='Lista de dicionários com nome e editável de cada coluna (apenas para tipo genérico)'
    )

    class Meta:
        verbose_name = 'Planilha'
        verbose_name_plural = 'Planilhas'

    def __str__(self):
        return f"{self.board.nome} - {self.nome}"