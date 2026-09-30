import asyncio
import json
from contextvars import ContextVar
import payments

request_id_var = ContextVar("request_id", default="-")


def log(event, **fields):
    print(json.dumps({
        "service": "checkout-svc",
        "request_id": request_id_var.get(),
        "event": event,
        **fields,
    }))


ORDERS = [
    ("O-1001", 42.00),
    ("O-1002", 15.50),
    ("O-1003", 88.00),
    ("O-1004", 23.25),
    ("O-1005", 61.10),
]


async def charge_card(order_id, amount, attempt):
    await asyncio.sleep(0)
    log("charge_success", order_id=order_id, amount=amount)
    if order_id == "O-1003" and attempt == 1:
        log("confirmation_dropped", order_id=order_id)
        return False
    return True


async def order_flow(order_id, amount):
    request_id_var.set(f"req-{order_id}")
    log("order_received", order_id=order_id, amount=amount)
    ok = await charge_card(order_id, amount, attempt=1)
    if not ok:
        log("retrying_charge", order_id=order_id)
        await charge_card(order_id, amount, attempt=2)
    log("order_complete", order_id=order_id)
    headers = {"X-Request-Id": request_id_var.get()}
    payments.handle_confirmation(headers, order_id)


async def main():
    await asyncio.gather(
        *(order_flow(oid, amt) for oid, amt in ORDERS)
    )


asyncio.run(main())
