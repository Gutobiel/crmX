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
    return render(request, 'board/new_board.html', {'workspaces': workspaces})


def workspace_detail(request, workspace_id):
    """Renderiza a página de detalhe da área de trabalho (lista de boards desse workspace)."""
    from workspaces.models import Workspace

    workspace = Workspace.objects.filter(id=workspace_id).first()
    if not workspace:
        # redireciona para a listagem de workspaces se não existir
        return render(request, 'workspace/workspace.html', {'error': 'Área de trabalho não encontrada.'})

    # boards relacionados (related_name='boards' no modelo)
    boards = workspace.boards.all().order_by('nome')

    return render(request, 'workspace/detail.html', {
        'workspace': workspace,
        'boards': boards,
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