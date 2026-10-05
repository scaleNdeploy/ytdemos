import logging
import os

from logsetup import setup

log = logging.getLogger("notify")
API = "https://carrier.example/v1/notify"

def send(url, headers, body):
    return 200  # stand-in for the real HTTP call

def notify(order_id):
    token = os.environ["CARRIER_TOKEN"]
    headers = {"Authorization": f"Bearer {token}"}
    log.debug("headers=%s", headers)  # 2 a.m. debug line
    status = send(API, headers, {"order": order_id})
    log.info("order %s sent: %s", order_id, status)

if __name__ == "__main__":
    setup()
    notify("A-1042")
