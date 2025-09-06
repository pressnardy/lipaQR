from django.urls import path
from waiters import views, authentications

app_name = 'waiters'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', authentications.login_view, name='login'),
    path('logout/', authentications.logout_view, name='logout'),
    path('get_order', views.get_order, name='get_order'),
    path('get_menu/', views.get_menu, name='get_menu'),
    path('place_order/', views.place_order, name='place_order'),
    path('order_placed', views.order_placed, name='order_placed'),
    path('access_denied/', views.access_denied, name='access_denied'),
    path('order_failed/', views.order_failed, name='order_failed'),
    path('create_waiter/', views.create_waiter, name='create_waiter'),
    path('waiters/', views.waiters, name='waiters'),
    path('view_waiter/<int:waiter_id>', views.view_waiter, name='view_waiter'),
    path('waiters_dash/', views.waiters_dash, name='waiters_dash'),
    path('waiter_dash/<int:waiter_id>/', views.waiters_dash, name='view_waiter'),
]

