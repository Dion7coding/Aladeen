from django.contrib import admin
from django.utils import timezone
from .models import UPIAccount, OrderPayment
@admin.register(UPIAccount)
class UPIAccountAdmin(admin.ModelAdmin):
    list_display = ("upi_id", "is_active", "created_at")

    def save_model(self, request, obj, form, change):
        if obj.is_active:
            UPIAccount.objects.filter(is_active=True).update(is_active=False)
        super().save_model(request, obj, form, change)
@admin.register(OrderPayment)
class OrderPaymentAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "payment_status",
        "submitted_at",
        "verified_at",
    )
    list_filter = ("payment_status",)
    actions = ["approve_payment"]

    def approve_payment(self, request, queryset):
        updated = 0
        for payment in queryset:
            if payment.payment_status == "PENDING_VERIFICATION":
                payment.payment_status = "PAID"
                payment.verified_at = timezone.now()
                payment.save()
                updated += 1

        self.message_user(
            request,
            f"{updated} payment(s) approved successfully."
        )

    approve_payment.short_description = "Approve selected payments"
