from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout


def login_view(request, section):
    if request.user.is_authenticated:
        logout(request)
        return redirect('admins:login', section=section)
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if user := authenticate(request, username=username, password=password):
            login(request, user)
            return redirect('admins:section', section=section)
        return render(request, 'admins/login.html', {"error": "Invalid credentials"})
    return render(request, 'admins/login.html', {'section': section})


def dashboard_login(request):
    return login_view(request=request, section=None)

def drinks_login(request):
    section = 'drinks'
    return login_view(request=request, section=section)

def food_login(request):
    return login_view(request=request, section='food')

def waiters_login(request):
    return login_view(request=request, section='waiters')

