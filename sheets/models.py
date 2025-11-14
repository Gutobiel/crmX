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
    # Campos JSONField mantidos para compatibilidade/migração gradual
    colunas = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Configuração das Colunas (deprecated)',
        help_text='Use o modelo Column relacionado'
    )

    linhas = models.JSONField(
        default=list,
        blank=True,
        verbose_name='Linhas de Dados (deprecated)',
        help_text='Use o modelo Row relacionado'
    )

    class Meta:
        verbose_name = 'Planilha'
        verbose_name_plural = 'Planilhas'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.board.nome} - {self.nome}"


class Column(models.Model):
    """Representa uma coluna da planilha"""
    sheet = models.ForeignKey(
        Sheet,
        on_delete=models.CASCADE,
        related_name='columns',
        verbose_name='Planilha'
    )
    nome = models.CharField(
        max_length=255,
        verbose_name='Nome da Coluna'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem'
    )
    editavel = models.BooleanField(
        default=True,
        verbose_name='Editável'
    )

    class Meta:
        verbose_name = 'Coluna'
        verbose_name_plural = 'Colunas'
        ordering = ['sheet', 'order']
        unique_together = ['sheet', 'order']

    def __str__(self):
        return f"{self.nome} ({self.sheet.nome})"


class Row(models.Model):
    """Representa uma linha da planilha (principal ou sub-linha)"""
    sheet = models.ForeignKey(
        Sheet,
        on_delete=models.CASCADE,
        related_name='rows',
        verbose_name='Planilha'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='subrows',
        null=True,
        blank=True,
        verbose_name='Linha Pai'
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name='Ordem'
    )
    is_subrow = models.BooleanField(
        default=False,
        verbose_name='É Sub-linha'
    )

    class Meta:
        verbose_name = 'Linha'
        verbose_name_plural = 'Linhas'
        ordering = ['sheet', 'order']

    def __str__(self):
        if self.is_subrow:
            return f"Sub-linha #{self.id} da linha {self.parent_id}"
        return f"Linha #{self.id} da tabela {self.sheet.nome}"


class Cell(models.Model):
    """Representa uma célula da planilha"""
    row = models.ForeignKey(
        Row,
        on_delete=models.CASCADE,
        related_name='cells',
        verbose_name='Linha'
    )
    column = models.ForeignKey(
        Column,
        on_delete=models.CASCADE,
        related_name='cells',
        verbose_name='Coluna'
    )
    value = models.TextField(
        blank=True,
        default='',
        verbose_name='Valor'
    )

    class Meta:
        verbose_name = 'Célula'
        verbose_name_plural = 'Células'
        unique_together = ['row', 'column']

    def __str__(self):
        return f"({self.row_id}, {self.column.nome}) = {self.value}"