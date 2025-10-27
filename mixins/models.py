from datetime import timezone
from django.db import models

class TimestampMixin(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de Criação'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Última Alteração'
    )

    class Meta:
        abstract = True  # Não cria tabela/físico para esse model!

class ActiveMixin(models.Model):
    ativo = models.BooleanField(
        default=True,
        verbose_name="Ativo"
    )

    class Meta:
        abstract = True


class SoftDeleteMixin(models.Model):
    deleted_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Deletado em"
    )

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = timezone.now()
        self.save()

    class Meta:
        abstract = True

class NotesMixin(models.Model):
    anotacao = models.TextField(
        blank=True,
        null=True,
        verbose_name="Anotação"
    )

    class Meta:
        abstract = True

