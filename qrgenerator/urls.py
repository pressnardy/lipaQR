from django.urls import path
from . import views 
from . import views_dashbord

app_name = 'qrgenerator'

urlpatterns = [
    path('', views.index, name='index'),
    path('account/', views.account, name='account'),
    # path('<int:restaurant_id>/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_View, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('add_restaurant/', views.add_restaurant, name='add_restaurant'),
    path('add_item/', views_dashbord.add_item, name='add_item'),
    path('order/', views.order, name='order'),
    path('menu/', views_dashbord.menu_view, name='menu'),
    path('menu/<int:item_id>/', views_dashbord.menu_view, name='view_item'),
    path('edit_item/<int:item_id>/', views_dashbord.edit_item, name='edit_item'),
    path('remove_item/', views_dashbord.remove_item, name='remove_item'),
    path('paid/', views_dashbord.paid_orders, name='paid'),
    path('paid/<int:order_id>', views_dashbord.paid_orders, name='paid'),
    path('pending/', views_dashbord.pending_orders, name='pending'),
    path('pending/<int:order_id>/', views_dashbord.pending_orders, name='pending'),
    path('qr_images/', views.get_qr_codes, name='get_qrs'),
    path('new_orders/', views_dashbord.new_orders, name='new_orders'),
    path('mark_paid/', views_dashbord.mark_paid, name='mark_paid'),
    path('create_order/<int:restaurant_id>/', views_dashbord.create_order, name='create_order'),
    path('orders/', views_dashbord.orders, name='orders'),
    path('orders/<int:order_id>/', views_dashbord.orders, name='view_order'),
    path("search_order/", views_dashbord.search_order, name='search_order'),
]

