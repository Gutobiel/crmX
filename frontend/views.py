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

def logout_view(request):
    logout(request)
    return redirect('login')
