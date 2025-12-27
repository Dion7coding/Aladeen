from django.urls import path
from .views import AdminOrderDetailAPI, AdminOrdersListAPI, admin_login

urlpatterns = [
    path("login/", admin_login),
    
    path("orders/", AdminOrdersListAPI.as_view()),
      path("orders/<int:id>/", AdminOrderDetailAPI.as_view()),
]
