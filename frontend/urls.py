from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    # Quando acessar a raiz do site, redireciona para a página de login
    path('', RedirectView.as_view(url='/login/', permanent=False), name='root-redirect'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),

    path("home2/", views.home2, name="home2"),
    path("login2/", views.login_page, name="login_page"),
]
