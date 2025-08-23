from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from menus.models import Restaurant, Order, Item
from django.contrib.auth.decorators import login_required
from qrgenerator.forms import AddItemForm, EditItemForm
from menus import util


def menu_view(request, item_id=None):
    if restaurant := request.user.restaurant:
        items = restaurant.items.all().order_by('-item_id')
        context = {
            'items': items, 'restaurant': restaurant, 'display_item': items.first(),
            } 
        if item_id and (display_item := items.filter(item_id=item_id).first()):
            context['display_item'] = display_item
        return render(request, 'qrgenerator/menu.html', context)
    return redirect('qrgenerator:login')


def view_item(request, item_id):
    return redirect('menu', item_id)


def add_item(request):
    context = {'items': request.user.restaurant.menu}
    if request.method == 'POST':
        form = AddItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.restaurant = request.user.restaurant
            form.save()
            context['message'] = f"{form.instance.name} saved successfully"
            context['form'] = form
        return render(request, 'qrgenerator/add_item.html', context)
    context['form'] = AddItemForm()
    return render(request, 'qrgenerator/add_item.html', context)
        

def remove_item(request):
    context = {}
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        item = Item.get(item_id)
        if item.restaurant.created_by == request.user:
            item.delete()
            context['message'] = f"item deleted successfully"
            return redirect('qrgenerator:menu')
        return HttpResponseForbidden('Forbidden')
    

def edit_item(request, item_id):
    context = {}
    context['items'] = request.user.restaurant.items.all().order_by('-item_id')
    item = Item.get(item_id=item_id)
    if not item:
        context['message'] = f"Item does not exist"
    if request.method == 'POST' and item:
        form = EditItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('qrgenerator:view_item', item_id)
        context['form'] = form
    context['form'] = EditItemForm(instance=item)
    return render(request, 'qrgenerator/edit_item.html', context)


def mark_paid(request):
    context = {}
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.get(order_id=order_id)
        if order and order.restaurant.created_by == request.user:
            order.mark_paid()
            context['message'] = f"order set to paid"
            return render(request, 'qrgenerator/menu.html', context)
        return HttpResponseForbidden('Access Denied')
    return render(request, 'qrgenerator/menu.html')


def paid_orders(request, order_id=None):
    restaurant = request.user.restaurant
    if not restaurant:
        return HttpResponseForbidden('Access Denied')
    orders = restaurant.orders.filter(paid=True).order_by('-order_id')
    context = {
        'orders': orders, 'display_order': orders.first(), 'restaurant': restaurant,
        }
    if order_id:
        if display_order := Order.get(unique_value=order_id):
            display_order.new = False
            display_order.save()
            context['display_order'] = display_order
    return render(request, 'qrgenerator/paid.html', context)


def pending_orders(request, order_id=None):
    restaurant = request.user.restaurant
    if not restaurant:
        return HttpResponseForbidden('Access Denied')
    orders = restaurant.orders.filter(paid=False).order_by('-order_id')
    context = {
        'orders': orders, 'display_order': orders.first(), 'restaurant': restaurant,
        }
    if order_id and (display_order := Order.get(unique_value=order_id)):
        display_order.new = False
        display_order.save()
        context['display_order'] = display_order
    return render(request, 'qrgenerator/pending.html', context)


def get_qr_codes(request):
    ...


def new_orders(request):
    if restaurant := request.user.restaurant:
        orders = restaurant.new_orders()
        paid = len(orders['paid'])
        pending = len(orders['pending'])
        print(paid)
        return JsonResponse({'paid': paid, 'pending': pending})


def mark_paid(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        order = Order.get(unique_value=int(order_id))

        if not order.restaurant.created_by == request.user:
            return redirect('qrgenerator:login')
        order.paid = True
        order.save()
        return redirect('qrgenerator:paid', order_id=order_id)


def create_order(request, restaurant_id):
    if request.method == 'POST':
        table_number = request.POST.get('table_number')
        return redirect('menus:get_menu', restaurant_id=restaurant_id, table_number=table_number)
    return render(request, 'qrgenerator/create_order.html')
