# orders.py  (version one, the OLD code)
VERSION = "v1"
SAFETY = 5000  # my cap, so this laptop survives


def done(order, sent):
    return False  # old bug: never says "stop"


def handle(order):
    if order.get("fast"):  # old meaning: repeat the order
        sent = 0
        while not done(order, sent) and sent < SAFETY:
            sent += 1
        return sent, "repeat"
    return 1, "normal"
