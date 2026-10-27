from pricing import order_total


def test_save20_at_exactly_100():
    assert order_total(1, 100, coupon="SAVE20") == 80


def test_save20_just_below_100():
    assert order_total(1, 99, coupon="SAVE20") == 99


def test_save10_still_works():
    assert order_total(1, 50, coupon="SAVE10") == 45
