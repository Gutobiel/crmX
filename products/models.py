from django.db import models
from mixins.models import TimestampMixin

class Product(TimestampMixin, models.Model):
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome'
    )
    descricao = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descrição'
    )
    valor_unitario = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Valor Unitário',
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome