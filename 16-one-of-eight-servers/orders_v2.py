# orders.py  (version two, the NEW code)
VERSION = "v2"


def handle(order):
    if order.get("fast"):  # new meaning: use the fast lane
        return 1, "fast"
    return 1, "normal"
