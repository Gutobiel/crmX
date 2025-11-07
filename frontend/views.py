from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import JsonResponse
import jwt
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q, Count
from workspaces.models import Workspace

def jwt_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        token = None
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        else:
            # Fallback: tenta obter token de cookie (ex.: 'access_token')
            token = request.COOKIES.get('access_token') or request.COOKIES.get('access')
            if not token:
                return redirect('login')
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            # Tenta associar o usuário autenticado ao request
            user_id = payload.get('user_id') or payload.get('uid')
            if user_id:
                User = get_user_model()
                try:
                    request.user = User.objects.get(pk=user_id)
                except User.DoesNotExist:
                    request.user = AnonymousUser()
        except jwt.ExpiredSignatureError:
            return redirect('login')
        except jwt.InvalidTokenError:
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view

def login_view(request):
    return render(request, 'login/login.html')

@jwt_required
def home(request):
    return render(request, 'home/home.html')

@jwt_required
def workspace(request):
    if not request.user.is_authenticated:
        return redirect('login')
    # Renderiza página; dados serão carregados via API /api/v1/workspace/ com RQL no JS
    return render(request, 'workspace/workspace.html', {
        'current_user_id': request.user.id,
    })

def new_workspace(request):
    return render(request, 'workspace/new_workspace.html')

def board(request):
    return render(request, 'board/board.html')

def new_board(request):
    # Pass available workspaces to the new board form so the user can choose
    from workspaces.models import Workspace

    workspaces = Workspace.objects.all().order_by('nome')
    workspace_id = request.GET.get('workspace')  # Get workspace from URL parameter
    
    return render(request, 'board/new_board.html', {
        'workspaces': workspaces,
        'selected_workspace_id': workspace_id
    })


@jwt_required
def workspace_detail(request, workspace_id):
    """Renderiza a página de detalhe da área de trabalho (lista de boards desse workspace)."""
    from workspaces.models import Workspace, WorkspaceMember

    workspace = Workspace.objects.filter(id=workspace_id).prefetch_related(
        'boards', 
        'workspace_members__user__profile',
        'dono__profile'
    ).first()
    
    if not workspace:
        return render(request, 'workspace/workspace.html', {'error': 'Área de trabalho não encontrada.'})

    # Verifica se o usuário tem acesso
    is_owner = workspace.dono == request.user
    is_member = WorkspaceMember.objects.filter(workspace=workspace, user=request.user).exists()
    
    if not is_owner and not is_member:
        return render(request, 'workspace/workspace.html', {'error': 'Você não tem acesso a esta área de trabalho.'})

    # boards relacionados (related_name='boards' no modelo)
    boards = workspace.boards.all().order_by('nome')

    # Prepara lista de membros para o template
    members = []
    if workspace.dono:
        name = workspace.dono.get_full_name() or workspace.dono.username
        name_parts = name.split()
        initials = f"{name_parts[0][0]}{name_parts[-1][0]}".upper() if len(name_parts) >= 2 else name[0:2].upper()
        
        members.append({
            'id': workspace.dono.id,
            'name': name,
            'email': workspace.dono.email,
            'initials': initials,
            'is_owner': True
        })
    
    for wm in workspace.workspace_members.all():
        name = wm.user.get_full_name() or wm.user.username
        name_parts = name.split()
        initials = f"{name_parts[0][0]}{name_parts[-1][0]}".upper() if len(name_parts) >= 2 else name[0:2].upper()
        
        members.append({
            'id': wm.user.id,
            'name': name,
            'email': wm.user.email,
            'initials': initials,
            'is_owner': False
        })

    return render(request, 'workspace/detail.html', {
        'workspace': workspace,
        'boards': boards,
        'members': members,
        'is_owner': is_owner,
    })

@jwt_required
def board_detail(request, board_id):
    """Renderiza a página de detalhe de uma pasta específica (planilha)."""
    from boards.models import Board
    
    board = Board.objects.filter(id=board_id).select_related('workspace').first()
    if not board:
        return redirect('workspace')
    
    return render(request, 'board/detail.html', {
        'board': board,
        'workspace': board.workspace,
    })

def logout_view(request):
    # Para JWT, apenas limpar cookies no cliente já é suficiente.
    # Como boa prática, limpamos cookies também no servidor.
    response = redirect('login')
    try:
        response.delete_cookie('access')
        response.delete_cookie('access_token')
    except Exception:
        pass
    # Se houver sessão Django, finaliza
    logout(request)
    return response

def home2(request):
    return render(request, "home/home2.html")


def login_page(request):
    return render(request, "login/login2.html")