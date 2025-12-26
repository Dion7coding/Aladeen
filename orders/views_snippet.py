def decrease_cart(request, snack_id):
    cart = request.session.get('cart', {})
    snack_id_str = str(snack_id)
    
    if snack_id_str in cart:
        if cart[snack_id_str] > 1:
            cart[snack_id_str] -= 1
        else:
            del cart[snack_id_str]
        request.session['cart'] = cart
        messages.success(request, "Updated cart")
    
    return redirect('menu')
