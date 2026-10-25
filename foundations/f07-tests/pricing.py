"""F7: a tiny piece of business logic worth testing."""


def order_total(quantity, price_each, coupon=None):
    """Total price in dollars. The SAVE10 coupon takes 10% off orders of $50 or more."""
    total = quantity * price_each
    if coupon == "SAVE10" and total >= 50:
        total = round(total * 0.9, 2)
    return total
