from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

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


def incomming_orders(request, section):
        restaurant = get_restaurant(request)
        orders = restaurant.new_orders()
        all_order = [
            {'id': i.order_id, 'phoneNumber': i.phone_number, 'totalAmount': i.total_amount}
                     for i in orders['all']
            ]
        paid = len(orders['paid'])
        pending = len(orders['pending'])
        print(paid)
        return JsonResponse({'paid': paid, 'pending': pending, 'all': all_order})

