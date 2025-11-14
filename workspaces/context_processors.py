from django.db.models import Q
from .models import Workspace

def workspaces_context(request):
    """Adiciona workspaces do usuário (como dono ou membro) ao contexto."""
    ctx = {
        'workspaces': [],
        'user_workspaces': [],
        'active_workspace': None,
    }
    if not request.user.is_authenticated:
        return ctx

    qs = Workspace.objects.filter(Q(dono=request.user) | Q(membros=request.user)).distinct().order_by('nome')
    ctx['workspaces'] = list(qs)
    ctx['user_workspaces'] = ctx['workspaces']

    # Detecta workspace ativo pela URL, se aplicável
    match = getattr(request, 'resolver_match', None)
    if match:
        workspace_id = match.kwargs.get('workspace_id')
        if workspace_id:
            ctx['active_workspace'] = qs.filter(id=workspace_id).first()

    return ctx
