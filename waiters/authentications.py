from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect


def login_view(request):
    if request.user.is_authenticated:
        return redirect('waiters:get_menu')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if user := authenticate(request, username=username, password=password):
            login(request, user)
            return redirect('waiters:get_menu')
        return render(request, 'waiters/login.html', {"error": "Invalid credentials"})
    return render(request, 'waiters/login.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('waiters:index')
    
