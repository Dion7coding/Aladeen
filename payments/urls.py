from django.urls import path
from . import views

urlpatterns = [
    path("upi/pay/<int:order_id>/", views.upi_redirect, name="upi_pay"),
    path("upi/confirm/<int:order_id>/", views.confirm_payment, name="upi_confirm"),
    path('my-orders/', views.my_orders, name='my_orders'),

]
