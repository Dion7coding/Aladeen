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
