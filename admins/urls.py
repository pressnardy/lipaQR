from django.urls import path
from admins import views, auths
app_name = 'admins'

urlpatterns = [
    path('', views.index, name='index'),
    path('waiters_login/', auths.waiters_login, name='waiters_login'),
    path('food_login/', auths.food_login, name='food_login'),
    path('drinks_login/', auths.drinks_login, name='drinks_login'),
    path('dashboard_login/', auths.dashboard_login, name='dashboard_login'),
    path('login/<str:section>/', auths.login_view, name='login'),
    # path('food/', views.food, name='food'),
    # path('drinks/', views.drinks, name='drinks'),
    path('<str:section>/', views.section, name='section'),
    path('view_waiter/<str:section>/<int:waiter_id>/', views.waiter_dashboard, name='view_waiter'),
    path('view_order/<str:section>/<int:order_id>/', views.order_dashboard, name='view_order'),
]
