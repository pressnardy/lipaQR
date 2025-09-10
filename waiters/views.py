from django.shortcuts import render, redirect
from django.http import HttpResponse
from menus.models import Waiter
from menus import views as menus_views
from waiters.forms import OrderForm, CreateWaiterForm
from utilities import constants, util
from waiters.authentications import login_view
# Create your views here.

def authenticate_request(request):
    if request.user.id is None:
        return redirect('waiters:login')
    return True


def get_restaurant(request):
    authenticate_request(request)
    try:
        if restaurant := request.user.restaurant:
            return restaurant
        return redirect('qrgenerator:add_restaurant')
    except Exception as e:
        return HttpResponse('Restaurant Validation Error', status=404)


def order_placed(request):
    return render(request, 'waiters/order_placed.html')


def index(request):
    return login_view(request)


def categorize(request, table_number):
    restaurant = get_restaurant(request)
    if request.method == 'POST':
        category = request.POST.get('category')
        table_number = request.POST.get('table_number')
        if category and table_number:
            return get_menu(request)
    return render(request, 'waiters/categories.html', {'table_number': table_number, 'restaurant': restaurant})


def get_table(request):
    table_number = request.POST.get('table_number')
    if table_number:
        return redirect('waiters:categorize', table_number=table_number)
    return render(request, 'waiters/get_table.html')


def get_menu(request):
    restaurant = get_restaurant(request)
    menu = restaurant.menu
    category = request.POST.get('category')
    table_number = request.POST.get('table_number')
    if not table_number:
        raise ValueError('missing table number')
    if category:
        menu = restaurant.menu_by_category(category)['items']
    context = {
        'restaurant': restaurant,
        'table_number': table_number,
        'menu': menu,
        'category': category,
    }
    return render(request, 'waiters/menu.html', context)
    

def get_order(request):
    if request.method == 'POST':
        order_details = [[k, v] for k, v in request.POST.items()]
        items = []
        for i in order_details[3:]:
            if i[1].isnumeric() and int(i[1]) > 0:
                item = {'item_id': i[0], 'item_quantity': i[1]}
                items.append(item)
        
        restaurant_id = get_restaurant(request).restaurant_id
        table_number = request.POST.get('table_number')
        restaurant, valid_items, invalid_items = util.get_order(restaurant_id, items)
        if valid_items:
            context = util.get_order_context(restaurant, valid_items, invalid_items, table_number)
            return render(request, 'waiters/order.html', context)
    return get_menu(request)


def place_order(request):
    form = OrderForm(request.POST)
    if not form.is_valid():
        return HttpResponse(form.errors)
        return redirect('waiters:get_order')
    raw_pin = request.POST.get('waiter_pin')
    restaurant = get_restaurant(request)
    form.instance.restaurant = restaurant
    waiter = Waiter.get(raw_pin=raw_pin, restaurant=restaurant)
    form.instance.created_by = waiter
    form.instance.phone_number = waiter.phone_number
    order = form.save()
    
    items = util.get_ordered_items(request.POST)
    pending = util.save_to_pending(items, order=order)
    # return HttpResponse(items)
    if pending:
        return order_placed(request)
    

def order_placed(request):
    return render(request, 'waiters/order_placed.html')


def access_denied(request):
    return render(request, 'waiters/access_denied.html')


def order_failed(request):
    return render(request, 'waiters/order_failed.html')

def waiter_added(request):
    ...
def create_waiter(request):
    restaurant = get_restaurant(request)
    context = {'restaurant':restaurant}
    if request.method == 'GET':
        return render(request, 'waiters/create_waiter.html', context=context)
    form = CreateWaiterForm(request.POST)
    if form.is_valid():
        form.instance.restaurant = restaurant
    if waiter := form.save():
        context['message'] = 'waiter added successfully'
    else:
        context['error'] = form.errors.items()
    return render(request, 'waiters/create_waiter.html', context=context)
    

def waiters(request):
    restaurant = get_restaurant(request)
    waiters = restaurant.all_waiters()
    context = {'restaurant': restaurant, 'waiters': waiters}
    return render(request, 'waiters/waiters.html', context)


def view_waiter(request, waiter_id):
    resttaurant = get_restaurant(request)
    waiter = Waiter.get(id=waiter_id)
    context = {
        'waiter': waiter,
        'restaurant': resttaurant,
    }
    return render(request, 'waiters/waiter_dash.html', context)


def waiters_dash(request, waiter_id=None):
    restaurant = get_restaurant(request)
    waiters = restaurant.waiters.all()
    filter_by = request.POST.get('filter_by') or 'all'
    waiter_id = request.POST.get('waiter_id') or waiter_id
    context = {'restaurant': restaurant, 'waiters': waiters, 'filter_by': filter_by}

    display_waiter = Waiter.get(restaurant=restaurant, id=waiter_id) or waiters.first()
    if display_waiter:
        waiter_orders = display_waiter.get_orders(filter_by=filter_by)
        context['display_waiter'] = display_waiter
        context['orders'] = waiter_orders
    return render(request, 'waiters/waiter_dash.html', context)
