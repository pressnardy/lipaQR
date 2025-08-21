from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Order
from . import util
from .forms import OrderForm


# Create your views here.


def get_menu(request, restaurant_id, table_number):
    restaurant = util.get_restaurant(restaurant_id=restaurant_id)
    if not restaurant:
        return HttpResponse("Restaurant not found. Please scan again.", status=400)
    menu = restaurant.menu
    context = {
        'restaurant': restaurant,
        'table_number': table_number,
        'menu': menu,
    }
    return render(request, 'menus/menu.html', context)


def get_order(request, restaurant_id, table_number):
    if request.method == 'POST':
        order_details = [[k, v] for k, v in request.POST.items()]
        items = []
        for i in order_details[3:]:
            if i[1].isnumeric() and int(i[1]) > 0:
                item = {'item_id': i[0], 'item_quantity': i[1]}
                items.append(item)

        restaurant, valid_items, invalid_items = util.get_order(restaurant_id, items)
        if valid_items:
            context = util.get_order_context(restaurant, valid_items, invalid_items, table_number)
            return render(request, 'menus/order.html', context)
    return redirect('menus:get_menu', restaurant_id=restaurant_id, table_number=table_number)


def place_order(request, restaurant_id, table_number):
    form = OrderForm(request.POST)
    if form.is_valid():
        reference_number = form.cleaned_data['reference_number']
        form_restaurant_id = request.POST.get('restaurant_id')
        form_table_number = request.POST.get('table_number')
        if form_restaurant_id != str(restaurant_id) or form_table_number != str(table_number):
            return HttpResponse("Invalid restaurant or table number.", status=400)
        restaurant = util.get_restaurant(restaurant_id=restaurant_id)
        form.instance.restaurant = restaurant
        form.instance.table_number = form_table_number
        order = form.save()
        print(order)
        items = util.get_ordered_items(request.POST)
        util.save_to_pending(items, order=order)
        return redirect(
            'menus:pay_order', restaurant_id=restaurant_id, table_number=table_number,
            reference_number=reference_number
        )
    return redirect('menus:get_order', restaurant_id=restaurant_id, table_number=table_number)


def pay_order(request, restaurant_id, table_number, reference_number):
    order = Order.objects.filter(reference_number=reference_number).first()
    if not order:
        return redirect('menus:get_menu', restaurant_id=restaurant_id, table_number=table_number)
    if request.method == 'POST':
        restaurant = util.get_restaurant(restaurant_id=restaurant_id)
        if reference_number == request.POST.get('reference_number'):
            util.send_stk_push(restaurant, order, reference_number)
            return order_placed(request, order=order)
        return order_failed(request, order=order)
    return render(request, 'menus/pay.html', {'order': order})

def order_placed(request, order):
    return render(request, 'menus/order_placed.html', {'order': order})

def order_failed(request, order):
    return render(request, 'order_failed.html', {
        "restaurant_id": order.restaurant.restaurant_id, 
        "table_number": order.table_number,
        "order": order,
    })

def payment_success(request, paid_order):
    return render(request, 'menus/order_success.html', {'order': paid_order})


def payment_failed(request):
    return render(request, 'menus/payment_failed.html')
