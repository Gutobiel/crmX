from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ElementProduct

@receiver([post_save, post_delete], sender=ElementProduct)
def atualizar_totais_element(sender, instance, **kwargs):
    instance.elemento.atualizar_totais()
