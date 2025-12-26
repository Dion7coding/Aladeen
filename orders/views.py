from django.shortcuts import render, redirect, get_object_or_404
from .models import Snack, Order, OrderItem
from django.contrib import messages
from django.db import transaction


def landing_page(request):
    if request.method == 'POST':
        # Clear previous session data (cart, order_total, etc.)
        request.session.flush()
        
        lab_name = request.POST.get('lab_name')
        system_number = request.POST.get('system_number')
        if lab_name and system_number:
            request.session['user_info'] = {'lab_name': lab_name, 'system_number': system_number}
            return redirect('menu')
    return render(request, 'landing.html')

def menu(request):
    snacks = Snack.objects.filter(is_available=True)
    cart = request.session.get('cart', {})
    
    # Process cart to get quantities per snack for template
    snacks_with_qty = []
    for snack in snacks:
        qty = cart.get(str(snack.id), 0)
        snacks_with_qty.append({
            'snack': snack,
            'qty': qty
        })
        
    return render(request, 'menu.html', {'snacks_with_qty': snacks_with_qty})

def decrease_cart(request, snack_id):
    cart = request.session.get('cart', {})
    snack_id_str = str(snack_id)
    
    if snack_id_str in cart:
        if cart[snack_id_str] > 1:
            cart[snack_id_str] -= 1
        else:
            del cart[snack_id_str]
        request.session['cart'] = cart
    
    return redirect('menu')


def add_to_cart(request, snack_id):
    snack = get_object_or_404(Snack, id=snack_id)
    cart = request.session.get('cart', {})
    snack_id_str = str(snack_id)
    
    current_quantity = cart.get(snack_id_str, 0)
    
    if request.method == 'POST':
         # If coming from a manual input form, might be useful later. 
         # For now assuming +1 increment or simple add.
         pass

    if current_quantity + 1 > snack.stock:
        messages.error(request, f"Only {snack.stock} items available for {snack.name}")
        return redirect('menu')

    if snack_id_str in cart:
        cart[snack_id_str] += 1
    else:
        cart[snack_id_str] = 1
    request.session['cart'] = cart
    messages.success(request, "Added to cart")
    return redirect('menu')


def cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0
    for snack_id, quantity in cart.items():
        snack = get_object_or_404(Snack, id=snack_id)
        total += snack.price * quantity
        cart_items.append({'snack': snack, 'quantity': quantity, 'subtotal': snack.price * quantity})
    
    return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})

def remove_from_cart(request, snack_id):
    cart = request.session.get('cart', {})
    snack_id = str(snack_id)
    if snack_id in cart:
        del cart[snack_id]
        request.session['cart'] = cart
    return redirect('cart')

def checkout(request):
    user_info = request.session.get('user_info')
    if not user_info:
        return redirect('landing_page')
    
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('menu')

    cart_items = []
    total = 0
    for snack_id, quantity in cart.items():
        snack = get_object_or_404(Snack, id=snack_id)
        total += snack.price * quantity
        cart_items.append({'snack': snack, 'quantity': quantity, 'subtotal': snack.price * quantity})

    if request.method == 'POST':
        # Proceed to payment (mock)
        request.session['order_total'] = float(total)
        return redirect('payment')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total, 'user_info': user_info})

def payment(request):
    total = request.session.get('order_total', 0)
    if request.method == 'POST':
        # Create Order
        user_info = request.session.get('user_info')
        cart = request.session.get('cart', {})
        
        try:
            with transaction.atomic():
                order = Order.objects.create(
                    lab_name=user_info['lab_name'],
                    system_number=user_info['system_number'],
                    total_amount=total,
                    status='Pending',
                    payment_status=True # Mock success
                )
                
                for snack_id, quantity in cart.items():
                    # Re-fetch snack with lock to prevent race conditions ideally, 
                    # but simple get is fine for this scope.
                    snack = Snack.objects.select_for_update().get(id=snack_id)
                    
                    if snack.stock < quantity:
                        raise Exception(f"Insufficient stock for {snack.name}")
                    
                    snack.stock -= quantity
                    snack.save()

                    OrderItem.objects.create(
                        order=order,
                        snack=snack,
                        quantity=quantity,
                        price=snack.price
                    )
                
                # Clear cart only if successful
                del request.session['cart']
                if 'order_total' in request.session:
                    del request.session['order_total']
                    
                return redirect('order_success')
        except Exception as e:
            messages.error(request, str(e))
            return redirect('cart')
        
    return render(request, 'payment.html', {'total': total})


def order_success(request):
    return render(request, 'order_success.html')
