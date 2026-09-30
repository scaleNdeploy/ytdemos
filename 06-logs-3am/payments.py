import json
from contextvars import ContextVar

request_id_var = ContextVar("request_id", default="-")


def log(event, **fields):
    print(json.dumps({
        "service": "payments-svc",
        "request_id": request_id_var.get(),
        "event": event,
        **fields,
    }))


def handle_confirmation(headers, order_id):
    request_id_var.set(headers["X-Request-Id"])
    log("confirmation_received", order_id=order_id)
