from django.db.models.signals import post_save
from django.dispatch import receiver
from sheets.models import Sheet


@receiver(post_save, sender=Sheet)
def init_sheet_data(sender, instance: Sheet, created, **kwargs):
    """Mantido por compatibilidade retroativa; configuração inicial agora acontece no serializer."""
    return
