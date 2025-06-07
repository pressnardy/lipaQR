from django.urls import path
from .import views

app_name = 'mpesa'

urlpatterns = [
    path('stk', views.push_stk, name='stk_push'),
    path('callback', views.get_callback, name='callback'),
]
