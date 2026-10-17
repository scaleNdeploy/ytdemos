# orders.py  (version three: old code deleted, new name)
VERSION = "v3"


def handle(order):
    if order.get("fast_lane"):  # a brand new switch name
        return 1, "fast"
    return 1, "normal"
