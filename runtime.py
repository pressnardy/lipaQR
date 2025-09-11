import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lipaqr.settings')
django.setup()

from menus.models import Waiter

waiter = Waiter.objects.get(id=1)

order = waiter.orders.all().order_by('-order_id').first()
print(order.category)


