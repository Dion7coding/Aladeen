from django.shortcuts import redirect, render, get_object_or_404
from django.utils import timezone
from admin_api.notifications import notify_admin_payment
from orders.models import Order
from .models import UPIAccount, OrderPayment
def upi_redirect(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    payment, _ = OrderPayment.objects.get_or_create(order=order)

    # 🚫 If already submitted or verified, block
    if payment.payment_status != "CREATED":
        return render(request, "payments/pending.html")

    upi = UPIAccount.objects.filter(is_active=True).first()
    if not upi:
        return render(request, "payments/no_upi.html")

    reg_no = f"ALADEEN_{order.id}"

    upi_url = (
        f"upi://pay?"
        f"pa={upi.upi_id}&"
        f"pn=AladeenStore&"
        f"am={order.total_amount}&"
        f"cu=INR&"
        f"tn={reg_no}"
    )

    payment.upi_account = upi
    payment.save()

    return render(request, "payments/upi_redirect.html", {
        "upi_url": upi_url,
        "order": order
    })

def confirm_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    payment = get_object_or_404(OrderPayment, order=order)

    # 🚫 Block re-submission
    if payment.payment_status != "CREATED":
        return render(request, "payments/pending.html", {
            "order": order
        })

    payment.payment_status = "PENDING_VERIFICATION"
    payment.submitted_at = timezone.now()
    payment.save()
    notify_admin_payment(order)
    return render(request, "payments/pending.html", {
        "order": order
    })

def my_orders(request):
    user_info = request.session.get('user_info')
    if not user_info:
        return redirect('landing_page')

    orders = Order.objects.filter(
        lab_name=user_info['lab_name'],
        system_number=user_info['system_number']
    ).order_by('-id')

    return render(request, 'my_orders.html', {
        'orders': orders
    })
