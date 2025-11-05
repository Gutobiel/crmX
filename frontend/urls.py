from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Quando acessar a raiz do site, redireciona para a página de login
    path('', RedirectView.as_view(url='/login/', permanent=False), name='root-redirect'),
    path('login/', views.login_view, name='login'),

    path('home/', views.home, name='home'),

    path('workspace/', views.workspace, name='workspace'),
    path('workspace/new/', views.new_workspace, name='new_workspace'),
    path('workspace/<int:workspace_id>/', views.workspace_detail, name='workspace_detail'),

    path('board/', views.new_board, name='board'),
    path('board/new/', views.new_board, name='new_board'),

    path('logout/', views.logout_view, name='logout'),

    path("home2/", views.home2, name="home2"),
    path("login2/", views.login_page, name="login_page"),

]
