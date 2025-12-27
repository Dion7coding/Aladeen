from firebase_admin import messaging
from admin_api.models import AdminDevice

def notify_admin_payment(order):
    try:
        # Import inside try so backend never crashes
        from admin_api.firebase import init_firebase
        init_firebase()

        devices = AdminDevice.objects.all()
        if not devices.exists():
            return

        for device in devices:
            message = messaging.Message(
                notification=messaging.Notification(
                    title="Payment Submitted",
                    body=(
                        f"Order #{order.id} | "
                        f"Lab {order.lab_name} | "
                        f"₹{order.total_amount}"
                    ),
                ),
                data={
                    "order_id": str(order.id),
                    "event": "PAYMENT_PENDING",
                },
                token=device.device_token,
            )
            messaging.send(message)

    except Exception:
        # 🚫 NEVER break order flow due to push failure
        pass
