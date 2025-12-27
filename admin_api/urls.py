from django.urls import path
from .views import AdminOrdersListAPI, admin_login

urlpatterns = [
    path("login/", admin_login),
    
    path("orders/", AdminOrdersListAPI.as_view()),
]
