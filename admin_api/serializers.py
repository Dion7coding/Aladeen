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
