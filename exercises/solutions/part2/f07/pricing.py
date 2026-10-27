"""F7 your turn, solved: add SAVE20, 20% off orders of $100 or more."""


def order_total(quantity, price_each, coupon=None):
    total = quantity * price_each
    if coupon == "SAVE10" and total >= 50:
        total = round(total * 0.9, 2)
    elif coupon == "SAVE20" and total >= 100:
        total = round(total * 0.8, 2)
    return total
