# File: cart_utils.py

from .models import Cart

def recalculate_total_amount(cart):
    """
    Recalculates the total amount for the given cart based on its CartItems.
    """
    total_amount = sum(item.quantity * item.price_at_time for item in cart.cartitem_set.all())
    cart.total_amount = total_amount
    cart.save()
