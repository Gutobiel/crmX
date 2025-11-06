from django.db import migrations

def set_owner_for_null_workspaces(apps, schema_editor):
    Workspace = apps.get_model('workspaces', 'Workspace')
    User = apps.get_model('auth', 'User')
    try:
        user = User.objects.filter(username='gutobielsantos').first()
        if not user:
            return
        Workspace.objects.filter(dono__isnull=True).update(dono=user)
    except Exception:
        # Em caso de erro, não falhar a migração; apenas seguir adiante
        pass


def reverse_noop(apps, schema_editor):
    # Não revertido automaticamente
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('workspaces', '0004_merge_20251106_1537'),
    ]

    operations = [
        migrations.RunPython(set_owner_for_null_workspaces, reverse_noop),
    ]
