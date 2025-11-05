from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import JsonResponse
import jwt
from django.conf import settings
from django.contrib.auth import logout

def jwt_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return redirect('login')
        
        token = auth_header.split(' ')[1]
        
        try:
            jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return redirect('login')
        except jwt.InvalidTokenError:
            return redirect('login')
        
        return view_func(request, *args, **kwargs)
    
    return wrapped_view

def login_view(request):
    return render(request, 'login/login.html')

def home(request):
    return render(request, 'home/home.html')

def workspace(request):
    return render(request, 'workspace/workspace.html')

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
    logout(request)
    return redirect('login')

def home2(request):
    return render(request, "home/home2.html")


def login_page(request):
    return render(request, "login/login2.html")