from django.contrib.auth import authenticate

from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from .serializers import AdminOrderSerializer
from .permissions import IsAdminUserOnly


@api_view(['POST'])
def admin_login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    if not username or not password:
        return Response(
            {"error": "Username and password required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(username=username, password=password)

    if not user or not user.is_staff:
        return Response(
            {"error": "Invalid admin credentials"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    token, _ = Token.objects.get_or_create(user=user)
    return Response({"token": token.key})


class AdminOrdersListAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOnly]

    def get(self, request):
        orders = Order.objects.all().order_by("-created_at")
        serializer = AdminOrderSerializer(orders, many=True)
        return Response(serializer.data)
from django.shortcuts import get_object_or_404
from .serializers import AdminOrderDetailSerializer


class AdminOrderDetailAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOnly]

    def get(self, request, id):
        order = get_object_or_404(Order, id=id)
        serializer = AdminOrderDetailSerializer(order)
        return Response(serializer.data)
from django.utils import timezone
from payments.models import OrderPayment


class AdminApprovePaymentAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUserOnly]

    def post(self, request, id):
        payment = get_object_or_404(OrderPayment, order_id=id)

        if payment.payment_status == "PAID":
            return Response(
                {"message": "Payment already approved"},
                status=400
            )

        payment.payment_status = "PAID"
        payment.verified_at = timezone.now()
        payment.save()

        # Optional: mark order completed
        payment.order.status = "Completed"
        payment.order.save()

        return Response({"status": "PAID"})
