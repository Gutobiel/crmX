from workspaces.models import Workspace


def workspace_context(request):
    """
    Context processor to inject workspace data into all templates.
    Provides user_workspaces and active_workspace variables.
    """
    context = {
        'user_workspaces': [],
        'active_workspace': None,
    }
    
    # Only provide workspace data for authenticated users
    if request.user.is_authenticated:
        # Get all workspaces ordered by name
        context['user_workspaces'] = Workspace.objects.filter(ativo=True).order_by('nome')
        
        # Get active workspace from session
        active_workspace_id = request.session.get('active_workspace_id')
        if active_workspace_id:
            try:
                context['active_workspace'] = Workspace.objects.get(id=active_workspace_id, ativo=True)
            except Workspace.DoesNotExist:
                # Clear invalid workspace from session
                request.session.pop('active_workspace_id', None)
    
    return context
