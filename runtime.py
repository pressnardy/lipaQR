import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'lipaqr.settings')
django.setup()

from menus.models import Waiter

waiters = Waiter.objects.all()
for waiter in waiters:
    print(waiter.totals())

