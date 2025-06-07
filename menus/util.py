from .models import Restaurant, Order, Item, OrderedItem
import random
import string


def get_restaurant(restaurant_id):
    restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
    if not restaurant:
        return None
    return restaurant


def get_names(items_list):
    return [item.split('_')[1] for item in items_list]


def get_ids(items_list):
    return [item.split('')[0] for item in items_list]


def make_reference_number():
    letters = ''.join(random.choices(string.ascii_letters, k=8))
    digits = ''.join(random.choices(string.digits, k=5))
    combined = list(letters + digits)
    random.shuffle(combined)
    final_selection = ''.join(random.sample(combined, k=12))
    return final_selection


def get_order(restaurant_id, items):
    restaurant = Restaurant.objects.filter(restaurant_id=restaurant_id).first()
    invalid_items = []
    valid_items = []
    available_items = restaurant.menu

    for i in items:
        if item := available_items.filter(item_id=i['item_id']).first():
            i['item_price'] = item.item_price
            i['item_name'] = item.item_name
            i['item_total'] = float(item.item_price) * float(i['item_quantity'])
            valid_items.append(i)
        else:
            invalid_items.append(i)
    return restaurant, valid_items, invalid_items


def get_order_context(restaurant, valid_items, invalid_items, table_number):
    total_amount = sum(item['item_price'] for item in valid_items)
    reference_number = make_reference_number()
    invalid_items = invalid_items if len(invalid_items) > 0 else None
    summary = {
        'reference_number': reference_number,
        'table_number': table_number,
        'phone_number': '',
        'total_amount': total_amount,
        'restaurant_id': restaurant.restaurant_id,

    }
    return {
        'summary': summary, 'valid_items': valid_items, 'invalid_items': invalid_items, 'restaurant': restaurant,
        'table_number': table_number
    }


def get_ordered_items(post_data):
    post_data_list = [[k, v] for k, v in post_data.items()]
    items = [{'item_id': i[0], 'item_quantity': int(i[1])} for i in post_data_list[6:]]
    return items


def is_successful_payment(reference_number):
    # This function should check if the payment was successful.
    # For now, we will assume all payments are successful.
    return True


def save_to_pending(items, order):
    for i in items:
        item = Item.objects.filter(item_id=i['item_id']).first()
        quantity = i['item_quantity']
        ordered_item = OrderedItem(item=item, order=order, quantity=quantity)
        ordered_item.save()


def set_to_paid(items):
    for item in items:
        item.paid = True
        item.save()
