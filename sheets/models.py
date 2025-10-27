from django.db import models
from boards.models import Board
from mixins.models import TimestampMixin, NotesMixin

class Sheet(NotesMixin, TimestampMixin, models.Model):
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

    class Meta:
        verbose_name = 'Planilha'
        verbose_name_plural = 'Planilhas'

    def __str__(self):
        return f"{self.board.nome} - {self.nome}"