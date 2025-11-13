from django.db import models
from sheets.models import Sheet
from mixins.models import TimestampMixin, NotesMixin, ActiveMixin, SoftDeleteMixin

class Element(
    TimestampMixin,
    NotesMixin,
    ActiveMixin,
    SoftDeleteMixin,
    models.Model
):
    sheet = models.ForeignKey(
        Sheet,
        on_delete=models.CASCADE,
        related_name='elements',
        verbose_name='Planilha'
    )
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Elemento'
    )

    colunas = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Colunas/Valores Dinâmicos'
    )

    class Meta:
        verbose_name = 'Elemento Genérico'
        verbose_name_plural = 'Elementos Genéricos'

    def __str__(self):
        return self.nome


class ContratosElement(
    TimestampMixin,
    NotesMixin,
    ActiveMixin,
    SoftDeleteMixin,
    models.Model
):
    STATUS_CHOICES = [
        ('ativo', 'Ativo'),
        ('inativo', 'Inativo'),
        ('pendente', 'Pendente'),
        ('concluido', 'Concluído'),
    ]
    
    empresa = models.CharField(
        max_length=30,
        verbose_name="Empresa"
    )
    objeto = models.CharField(
        max_length=200,
        verbose_name="Objeto"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='ativo',
        verbose_name="Status"
    )
    qtd_total_itens = models.IntegerField(
        default=0,
        verbose_name="Qtd Total Itens"
    )
    valor_total_anterior = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Valor Total Anterior"
    )
    valor_total_reajustado = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0,
        verbose_name="Valor Total Reajustado"
    )


    class Meta:
        verbose_name = 'Elemento Contratos'
        verbose_name_plural = 'Elementos Contratos'

    def __str__(self):
        return f"{self.empresa} - {self.objeto}"

    def atualizar_totais(self):
        subelements = self.subelementos.all()
        self.qtd_total_itens = sum(s.quantidade for s in subelements)
        self.valor_total_anterior = sum(s.valor_total for s in subelements)
        self.valor_total_reajustado = sum(s.valor_total_reajustado for s in subelements)
        self.save()

class ElementCollaborator(TimestampMixin, ActiveMixin, SoftDeleteMixin, models.Model):
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        related_name='collaborators',
        verbose_name='Elemento'
    )
    nome = models.CharField(
        max_length=100,
        verbose_name='Nome do Colaborador'
    )
    
    grossSalary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Salário bruto'
    )

    benefit_food = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Auxílio Alimentação',
    )

    benefit_transport = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        verbose_name='Auxílio Transporte',
    )

    class Meta:
        verbose_name = 'Colaborador do Elemento'
        verbose_name_plural = 'Colaboradores do Elemento'

    def __str__(self):
        return f'{self.nome} ({self.element.nome})'
    

class ElementFreelancer(ElementCollaborator):
    class Meta:
        verbose_name = 'Freelancer'
        verbose_name_plural = 'Freelancers'