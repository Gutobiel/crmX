from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import JsonResponse
import jwt
from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q, Count, Prefetch
from django.forms import HiddenInput
from workspaces.models import Workspace
from elements.models import ContratosElement
from elements.forms import ContratosElementForm

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
    # Carregar todos os contratos para a página home
    contratos = ContratosElement.objects.all().order_by('id')
    
    context = {
        'contracts': contratos,
    }
    return render(request, 'home/home.html', context)



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

def sheet_detail2(request):
    from sheets.models import Sheet
    from boards.models import Board

    sheet_id = request.GET.get('sheet') or request.GET.get('sheet_id')
    board_id = request.GET.get('board')

    sheet = None
    board = None
    workspace = None

    contratos_qs = ContratosElement.objects.all().select_related('sheet', 'board')

    if sheet_id:
        contratos_qs = contratos_qs.filter(sheet_id=sheet_id)
        sheet = Sheet.objects.filter(id=sheet_id).select_related('board__workspace').first()
        if sheet:
            board = sheet.board
            workspace = board.workspace if board else None
    elif board_id:
        contratos_qs = contratos_qs.filter(board_id=board_id)
        board = Board.objects.filter(id=board_id).select_related('workspace').first()
        if board:
            workspace = board.workspace

    if sheet and not board:
        board = sheet.board
        workspace = board.workspace if board else workspace

    initial = {}
    if sheet:
        initial['sheet'] = sheet
    if board:
        initial['board'] = board

    if request.method == 'POST':
        form = ContratosElementForm(request.POST, initial=initial)
    else:
        form = ContratosElementForm(initial=initial)

    sheet_queryset = Sheet.objects.select_related('board').all().order_by('nome')
    board_queryset = Board.objects.all().order_by('nome')

    if board:
        sheet_queryset = sheet_queryset.filter(board=board)

    form.fields['sheet'].queryset = sheet_queryset
    form.fields['board'].queryset = board_queryset

    if sheet:
        form.fields['sheet'].widget = HiddenInput()
    if board:
        form.fields['board'].widget = HiddenInput()

    if request.method == 'POST' and form.is_valid():
        selected_sheet = form.cleaned_data.get('sheet') or sheet
        selected_board = form.cleaned_data.get('board') or board

        if selected_sheet and not selected_board:
            selected_board = selected_sheet.board

        if not (selected_board or selected_sheet):
            form.add_error(None, 'Selecione uma pasta ou planilha válida para vincular o contrato.')
        else:
            contrato = form.save(commit=False)
            contrato.sheet = selected_sheet
            contrato.board = selected_board
            contrato.save()

            query_string = request.META.get('QUERY_STRING')
            redirect_url = request.path
            if query_string:
                redirect_url = f"{redirect_url}?{query_string}"
            return redirect(redirect_url)

    available_targets = bool(
        sheet or
        board or
        form.fields['board'].queryset.exists() or
        form.fields['sheet'].queryset.exists()
    )

    context = {
        'sheet': sheet,
        'board': board,
        'workspace': workspace,
        'contratos': contratos_qs.order_by('id'),
        'form': form,
        'can_add_contrato': available_targets,
        'show_board_field': board is None,
        'show_sheet_field': sheet is None,
    }

    return render(request, 'sheet/detail2.html', context)

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
def board_detail(request, workspace_id, board_id):
    """Renderiza a página de detalhe de uma pasta específica (planilha)."""
    from boards.models import Board
    from sheets.models import Sheet
    
    board = Board.objects.filter(id=board_id, workspace_id=workspace_id).select_related('workspace').first()
    if not board:
        # Se o workspace existir, redireciona para a listagem dele; caso contrário, volta para a página geral
        workspace_exists = Workspace.objects.filter(id=workspace_id).exists()
        if workspace_exists:
            return redirect('workspace_detail', workspace_id=workspace_id)
        return redirect('workspace')
    
    # Buscar planilhas do board
    sheets = Sheet.objects.filter(board=board).order_by('-created_at')
    
    # Debug
    print(f"DEBUG board_detail: Board ID={board.id}, Nome={board.nome}")
    print(f"DEBUG board_detail: Total de planilhas encontradas: {sheets.count()}")
    for sheet in sheets:
        print(f"  - Sheet ID {sheet.id}: {sheet.nome}")
    
    return render(request, 'board/detail.html', {
        'board': board,
        'workspace': board.workspace,
        'sheets': sheets,
        'workspace_id': workspace_id,
    })

@jwt_required
def new_sheet(request):
    """Renderiza a página de criação de nova planilha."""
    from boards.models import Board
    
    board_id = request.GET.get('board')
    if not board_id:
        return redirect('workspace')
    
    board = Board.objects.filter(id=board_id).select_related('workspace').first()
    if not board:
        return redirect('workspace')
    
    return render(request, 'sheet/new.html', {
        'board': board,
        'workspace': board.workspace,
    })

@jwt_required
def sheet_detail(request, sheet_id):
    """Renderiza a página de detalhe/edição de uma planilha."""
    from sheets.models import Sheet, Row, Cell

    sheet = Sheet.objects.filter(id=sheet_id).select_related(
        'board__workspace'
    ).first()

    if not sheet:
        return redirect('workspace')

    columns = list(sheet.columns.all().order_by('order'))

    subrows_prefetch = Prefetch(
        'subrows',
        queryset=Row.objects.order_by('order').prefetch_related(
            Prefetch('cells', queryset=Cell.objects.select_related('column'))
        )
    )

    rows_queryset = sheet.rows.filter(parent__isnull=True).order_by('order').prefetch_related(
        Prefetch('cells', queryset=Cell.objects.select_related('column')),
        subrows_prefetch
    )

    def serialize_row(row_instance):
        cell_map = {cell.column_id: cell for cell in row_instance.cells.all()}
        return {
            'id': row_instance.id,
            'is_subrow': row_instance.is_subrow,
            'parent_id': row_instance.parent_id,
            'cells': [
                {
                    'column_id': column.id,
                    'cell_id': cell_map[column.id].id if column.id in cell_map else None,
                    'value': cell_map[column.id].value if column.id in cell_map else ''
                }
                for column in columns
            ],
            'subrows': [serialize_row(subrow) for subrow in row_instance.subrows.all()]
        }

    rows_data = [serialize_row(row) for row in rows_queryset]

    return render(request, 'sheet/detail.html', {
        'sheet': sheet,
        'board': sheet.board,
        'workspace': sheet.board.workspace,
        'columns': columns,
        'sheet_rows': rows_data,
        'sheet_columns_count': len(columns),
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


@jwt_required
def sheet_contratos_detail(request, sheet_id):
    """Tela específica de contratos para uma planilha do tipo 'contratos'."""
    from sheets.models import Sheet

    sheet = Sheet.objects.filter(id=sheet_id).select_related('board__workspace').first()
    if not sheet:
        return redirect('workspace')

    board = sheet.board
    workspace = board.workspace if board else None

    # A página de contratos já usa o mesmo layout/JS de `home.html`/`contratos_detail.html`
    context = {
        'sheet': sheet,
        'board': board,
        'workspace': workspace,
    }
    return render(request, 'sheet/contratos_detail.html', context)