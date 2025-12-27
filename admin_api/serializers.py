from rest_framework import serializers
from orders.models import Order


class AdminOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "lab_name",
            "system_number",
            "total_amount",
            "status",
            "created_at",
        ]
from orders.models import OrderItem
from payments.models import OrderPayment


class AdminOrderItemSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="snack.name")

    class Meta:
        model = OrderItem
        fields = [
            "name",
            "quantity",
            "price",
        ]


class AdminOrderDetailSerializer(serializers.ModelSerializer):
    items = AdminOrderItemSerializer(many=True, read_only=True)
    payment_status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            "id",
            "lab_name",
            "system_number",
            "total_amount",
            "status",
            "payment_status",
            "items",
        ]

    def get_payment_status(self, obj):
        try:
            return obj.orderpayment.payment_status
        except OrderPayment.DoesNotExist:
            return "NOT_CREATED"
from orders.models import Snack


class AdminMenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Snack
        fields = [
            "id",
            "name",
            "price",
            "stock",
            "is_available",
        ]
from payments.models import UPIAccount


class AdminUPISerializer(serializers.ModelSerializer):
    class Meta:
        model = UPIAccount
        fields = [
            "id",
            "upi_id",
            "qr_code",
            "is_active",
        ]
