from django.urls import path
from admins import views
app_name = 'admins'

urlpatterns = [
    path('', views.index, name='index'),
    path('food/', views.food, name='food'),
    path('drinks/', views.drinks, name='drinks'),
    path('<str:section>/', views.section, name='section'),
    path('view_waiter/<str:section>/<int:waiter_id>/', views.waiter_dashboard, name='view_waiter'),
    path('view_order/<str:section>/<int:order_id>/', views.order_dashboard, name='view_order'),
]