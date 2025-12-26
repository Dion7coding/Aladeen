from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('menu/', views.menu, name='menu'),
    path('add-to-cart/<int:snack_id>/', views.add_to_cart, name='add_to_cart'),
    path('decrease-cart/<int:snack_id>/', views.decrease_cart, name='decrease_cart'),
    path('cart/', views.cart, name='cart'),

    path('remove-from-cart/<int:snack_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path("success/<int:order_id>/", views.order_success, name="order_success")

]
