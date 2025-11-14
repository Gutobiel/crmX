from django.db import models
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