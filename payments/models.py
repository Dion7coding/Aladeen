from django.db import models


class UPIAccount(models.Model):
    upi_id = models.CharField(max_length=100)
    qr_code = models.ImageField(upload_to="upi_qr/")
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.upi_id
class OrderPayment(models.Model):
    PAYMENT_STATUS = (
        ("CREATED", "Created"),
        ("PENDING_VERIFICATION", "Pending Verification"),
        ("PAID", "Paid"),
        ("FAILED", "Failed"),
    )

    order = models.OneToOneField(
        "orders.Order",
        on_delete=models.CASCADE
    )

    payment_status = models.CharField(
        max_length=30,
        choices=PAYMENT_STATUS,
        default="CREATED"
    )

    upi_account = models.ForeignKey(
        UPIAccount,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    submitted_at = models.DateTimeField(null=True, blank=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment for Order {self.order.id}"
    