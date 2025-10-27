from django.db import models
from elements.models import Element
from mixins.models import TimestampMixin
from elements.models import ContratosElement

class File(TimestampMixin, models.Model):
    element = models.ForeignKey(
        Element,
        on_delete=models.CASCADE,
        related_name='documentacao',
        verbose_name='Elemento'
    )
    file = models.FileField(
        upload_to='contratos_documentos/',
        verbose_name='Arquivo',
    )
    nome = models.CharField(
        max_length=100,
        verbose_name='Documentação'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Upload'
    )

    class Meta:
        verbose_name = 'Arquivo de Documentação'
        verbose_name_plural = 'Arquivos de Documentação'

    def __str__(self):
        return f'{self.element.nome}: {self.file.name}'


class ContratosElementFile(models.Model):
    element = models.ForeignKey(
        ContratosElement,
        on_delete=models.CASCADE,
        related_name='documentacao'
    )
    file = models.FileField(upload_to='contratos_documentos/')

    def __str__(self):
        return self.file.name
