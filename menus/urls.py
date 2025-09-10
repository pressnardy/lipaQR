from django.urls import path
from . import views, print_order


app_name = "menus"


urlpatterns = [
    path("<int:restaurant_id>/<int:table_number>/", views.get_menu, name="get_menu"),
    path("<int:restaurant_id>/", views.get_menu, name="restaurant_menu"),
    path("<int:restaurant_id>/<int:table_number>/get_order/", views.get_order, name="get_order"),
    path("<int:restaurant_id>/<int:table_number>/place_order/", views.place_order, name="place_order"),
    path("<int:restaurant_id>/<int:table_number>/<str:reference_number>/pay_order/", views.pay_order, name="pay_order"),
    path("<int:restaurant_id>/<int:table_number>/pay_order/<str:reference_number>/", views.payment_success, name="payment_success"),
    path("order_placed/", views.order_placed, name="order_placed"),
    path('print_order/<str:order_id>/', print_order.get_order, name='print_order'),
]

