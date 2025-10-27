from django.db import models
from django.contrib.auth.models import User
from mixins.models import TimestampMixin, ActiveMixin

class Workspace(TimestampMixin, ActiveMixin, models.Model):
    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nome da Área de Trabalho'
    )

    class Meta:
        verbose_name = 'Área de Trabalho'
        verbose_name_plural = 'Áreas de Trabalho'

    def __str__(self):
        return self.nome