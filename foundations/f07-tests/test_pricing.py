"""F7: tests are small programs that check your code still does what you promised.

Run:  uv run pytest foundations/f07-tests -v
"""

from pricing import order_total


def test_plain_order():
    assert order_total(3, 4) == 12


def test_coupon_applies_at_fifty_dollars():
    assert order_total(1, 50, coupon="SAVE10") == 45


def test_coupon_ignored_on_small_orders():
    assert order_total(2, 6, coupon="SAVE10") == 12


def test_unknown_coupon_changes_nothing():
    assert order_total(1, 80, coupon="FREE") == 80
