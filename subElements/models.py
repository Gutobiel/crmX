from django.db import models
from elements.models import Element
from products.models import Product
from mixins.models import TimestampMixin, NotesMixin, ActiveMixin, SoftDeleteMixin
from elements.models import ContratosElement

class SubElement(
    TimestampMixin,
    NotesMixin,
    ActiveMixin,
    SoftDeleteMixin,
    models.Model
):
    element = models.ForeignKey(
        'elements.Element',
        on_delete=models.CASCADE,
        related_name='subelements',
        verbose_name='Elemento Pai'
    )

    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Subelemento'
    )
    colunas = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Colunas/Valores Dinâmicos'
    )

    class Meta:
        verbose_name = 'Subelemento Genérico'
        verbose_name_plural = 'Subelementos Genéricos'

    def __str__(self):
        return f"{self.nome} ({self.element.nome})"


class ContratosSubelement(models.Model):
    element = models.ForeignKey(
        ContratosElement,
        on_delete=models.CASCADE,
        related_name='subElements'
    )
    nome = models.CharField(max_length=100, verbose_name="Nome do Subelemento")
    comentario = models.TextField(blank=True, null=True, verbose_name='Comentários')
    quantidade = models.IntegerField(verbose_name="Quantidade")
    valor_unitario_anterior = models.DecimalField(max_digits=15, decimal_places=2)
    valor_total = models.DecimalField(max_digits=15, decimal_places=2)
    valor_ipca = models.DecimalField(max_digits=7, decimal_places=2, verbose_name="Valor IPCA (%)")
    valor_unitario_reajustado = models.DecimalField(max_digits=15, decimal_places=2)
    valor_total_reajustado = models.DecimalField(max_digits=15, decimal_places=2)

    def save(self, *args, **kwargs):
        self.valor_total = self.quantidade * self.valor_unitario_anterior
        self.valor_unitario_reajustado = self.valor_unitario_anterior + (self.valor_unitario_anterior * (self.valor_ipca / 100))
        self.valor_total_reajustado = self.quantidade * self.valor_unitario_reajustado
        super().save(*args, **kwargs)
        if hasattr(self.element, 'atualizar_totais'):
            self.element.atualizar_totais()

    def delete(self, *args, **kwargs):
        element = self.element
        super().delete(*args, **kwargs)
        if element and hasattr(element, 'atualizar_totais'):
            element.atualizar_totais()

    class Meta:
        verbose_name = 'Subelemento Contratos'
        verbose_name_plural = 'Subelementos Contratos'

    def __str__(self):
        return f"{self.nome} | {self.element.objeto}"