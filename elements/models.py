from decimal import Decimal

from django.db import models
from django.db.models import Sum
from boards.models import Board

class Element(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='elements', null=True, blank=True)
    colunas = models.JSONField(default=dict, blank=True)
    sheet = models.ForeignKey('sheets.Sheet', on_delete=models.CASCADE, related_name='generic_elements', null=True, blank=True)
    
    class Meta:
        verbose_name = 'Elemento Genérico'
        verbose_name_plural = 'Elementos Genéricos'
    
    def __str__(self):
        return f"Elemento Genérico - Board {self.board.id if self.board else 'N/A'}"


class ContratosElement(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='contratos', null=True, blank=True)
    sheet = models.ForeignKey('sheets.Sheet', on_delete=models.CASCADE, related_name='contratos_elements', null=True, blank=True)
    elemento = models.CharField(max_length=255, blank=True, default='')
    empresa = models.CharField(max_length=255, blank=True, default='')
    objeto = models.TextField(blank=True, default='')
    qtd_total_itens = models.IntegerField(default=0, blank=True)
    valor_total_anterior = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    valor_total_reajustado = models.DecimalField(max_digits=15, decimal_places=2, default=0, blank=True)
    
    class Meta:
        verbose_name = 'Contrato'
        verbose_name_plural = 'Contratos'
    
    def __str__(self):
        return f"{self.elemento} - {self.empresa}" if self.elemento else f"Contrato #{self.id}"

    def atualizar_totais(self):
        aggregates = self.subElements.aggregate(
            total_anterior=Sum('valor_total'),
            total_reajustado=Sum('valor_total_reajustado'),
            quantidade_total=Sum('quantidade'),
        )

        self.valor_total_anterior = aggregates.get('total_anterior') or 0
        self.valor_total_reajustado = aggregates.get('total_reajustado') or 0
        self.qtd_total_itens = aggregates.get('quantidade_total') or 0
        self.save(update_fields=['valor_total_anterior', 'valor_total_reajustado', 'qtd_total_itens'])


class ElementCollaborator(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='collaborators', null=True, blank=True)
    sheet = models.ForeignKey('sheets.Sheet', on_delete=models.CASCADE, related_name='collaborator_elements', null=True, blank=True)
    element = models.CharField(max_length=255, blank=True, default='', verbose_name='Nome')
    cargo = models.CharField(max_length=255, blank=True, default='', verbose_name='Cargo')
    grossSalary = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, verbose_name='Salário Bruto')
    benefit_food = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, verbose_name='Benefício Alimentação')
    benefit_transport = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, verbose_name='Benefício Transporte')
    
    class Meta:
        verbose_name = 'Colaborador'
        verbose_name_plural = 'Colaboradores'
    
    def __str__(self):
        return f"{self.element} - {self.cargo}" if self.element else f"Colaborador #{self.id}"


class ProductElement(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    sheet = models.ForeignKey('sheets.Sheet', on_delete=models.CASCADE, related_name='product_elements', null=True, blank=True)
    codigo = models.CharField(max_length=100, blank=True, default='', verbose_name='Código')
    nome = models.CharField(max_length=255, blank=True, default='', verbose_name='Nome')
    categoria = models.CharField(max_length=255, blank=True, default='', verbose_name='Categoria')
    preco = models.DecimalField(max_digits=10, decimal_places=2, default=0, blank=True, verbose_name='Preço')
    estoque = models.IntegerField(default=0, blank=True, verbose_name='Estoque')
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
    
    def __str__(self):
        return f"{self.codigo} - {self.nome}" if self.codigo else f"Produto #{self.id}"