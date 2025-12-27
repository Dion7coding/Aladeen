from django.urls import path

from admin_api.models import AdminRegisterDeviceAPI, AdminUnregisterDeviceAPI
from .views import AdminApprovePaymentAPI, AdminMenuListAPI, AdminMenuUpdateAPI, AdminOrderDetailAPI, AdminOrdersListAPI, AdminUPIActivateAPI, AdminUPIListCreateAPI, admin_login

urlpatterns = [
    path("login/", admin_login),
    
    path("orders/", AdminOrdersListAPI.as_view()),
      path("orders/<int:id>/", AdminOrderDetailAPI.as_view()),
      path("orders/<int:id>/approve-payment/", AdminApprovePaymentAPI.as_view()),
      path("menu/", AdminMenuListAPI.as_view()),
    path("menu/<int:id>/", AdminMenuUpdateAPI.as_view()),
     path("upi/", AdminUPIListCreateAPI.as_view()),
    path("upi/<int:id>/activate/", AdminUPIActivateAPI.as_view()),
    path("register-device/", AdminRegisterDeviceAPI.as_view()),
path("unregister-device/", AdminUnregisterDeviceAPI.as_view()),

]
