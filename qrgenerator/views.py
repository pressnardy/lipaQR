from django.shortcuts import render, redirect
from django.http import HttpResponse
from .import generator
from menus.models import Restaurant
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from qrgenerator.forms import RegistrationForm, LoginForm, AddRestaurantForm, AddItemForm
from menus import util

def index(request):
    return render(request, 'qrgenerator/index.html')
    

def order(request):
    return render(request, 'qrgenerator/order.html')

def get_qr_codes(request):
    context = {}
    items = request.user.restaurant.items.all().order_by('-item_id')
    context['items'] = items
    if request.method == 'POST': 
        if restaurant := request.user.restaurant:
            total_tables = int(request.POST.get('tables'))
            restaurant_id = restaurant.restaurant_id
            generator.gen_images(total_tables, restaurant_id)
            qr_urls = [f'qrgenerator/{restaurant_id}/qr_code_{restaurant_id}{str(i + 1).zfill(2)}.png' for i in range(total_tables)]
            context['qr_urls'] = qr_urls
            context['restaurant'] = restaurant
            return render(request, 'qrgenerator/qr_images.html', context)
        context['message'] = f"Please add restaurant details to  proceed"
    return render(request, 'qrgenerator/get_qrs.html', context)


def login_View(request):
    if request.user.is_authenticated:
        return redirect('qrgenerator:account')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if user := authenticate(request, username=username, password=password):
            login(request, user)
            return redirect('qrgenerator:account')
        return render(request, 'qrgenerator/login.html', {"error": "Invalid credentials"})
    return render(request, 'qrgenerator/login.html')


def register(request):
    if request.user.is_authenticated:
        return redirect('qrgenerator:account')
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if util.is_existing(User, request.POST):
            errors = 'User Already Exists!!'
            return render('grgenerator/register.html', {'errors': errors})
        if not form.is_valid():
            return render('grgenerator/register.html', {'errors': form.errors})
        if user := form.save():
            login(request, user)
            return redirect('qrgenerator:add_restaurant')
    return render(request, 'qrgenerator/register.html')


def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('qrgenerator:index')


# @login_required
def account(request):
    return render(request, 'qrgenerator/dashbord.html')


def add_restaurant(request):
    if request.method == 'POST':
        form = AddRestaurantForm(request.POST)
        if form.is_valid():
            form.instance.created_by = request.user
            form.save()
            return redirect('qrgenerator:account')
        return render(request, 'qrgenerator/add_restaurant.html', {'form': form})
    return render(request, 'qrgenerator/add_restaurant.html')


    