from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from menus.models import Restaurant, Waiter, Order

def authenticate_request(request):
    if request.user.id is None:
        return redirect('admins:index')
    return True


def get_restaurant(request):
    authenticate_request(request)
    try:
        if restaurant := request.user.restaurant:
            return restaurant
        return redirect('qrgenerator:add_restaurant')
    except Exception as e:
        return HttpResponse('Restaurant Validation Error', status=404)

def get_orders_context(order_id, orders, restaurant):
    context = {
        'orders': orders, 'display_order': orders.first(), 'restaurant': restaurant,
        }
    if order_id and (display_order := Order.get(unique_value=order_id)):
        display_order.new = False
        display_order.save()
        context['display_order'] = display_order
    return context


def index(request):
    return redirect('admins:index')


@login_required(login_url='admins:index')
def dashboard(request, section, waiter_id=None, order_id=None):
    restaurant = get_restaurant(request)
    waiters = restaurant.waiters.all().order_by('id')
    display_waiter = waiters.first()
    orders = restaurant.orders.filter(category=section).order_by('-order_id')
    context = {}
    if waiter_id:
        display_waiter = restaurant.waiters.filter(id=waiter_id).first()
        orders = display_waiter.orders.filter(category=section).order_by('-order_id')
        context['display_waiter'] = display_waiter
    context.update(get_orders_context(order_id, orders, restaurant))
    context['waiters'] = waiters
    context['section'] = section
    return render(request, 'admins/dashboard.html', context)

def section(request, section):
    if section == 'food':
        return food(request)
    if section == 'drinks':
        return drinks(request)
    
def food(request):
    section = 'food'
    return dashboard(request, section)


def drinks(request):
    section ='drinks'
    return dashboard(request, section)


def waiter_dashboard(request, section, waiter_id):
    return dashboard(request, section, waiter_id=waiter_id)

def order_dashboard(request, section, order_id):
    print(section, order_id)
    return dashboard(request, section, order_id=order_id)
       
