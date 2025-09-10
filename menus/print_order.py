from menus.models import Order
from django.http import JsonResponse

def get_order(request, order_id):
    try:
        order = Order.objects.select_related('restaurant').prefetch_related('ordered_items').get(order_id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
    ordered_items = order.ordered_items.all()
    items = [{'name': item.name, 'total': item.price * item.quantity } for item in ordered_items]
    data = {
        'restaurantName': order.restaurant.name,
        'orderId': order.order_id,
        'tableNumber': order.table_number,
        'items': items,
    }
    return JsonResponse(data)
