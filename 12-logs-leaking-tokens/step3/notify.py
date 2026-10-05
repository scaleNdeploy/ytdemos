import logging
import os

from logsetup import setup

log = logging.getLogger("notify")
API = "https://carrier.example/v1/notify"
TRACK = "https://carrier.example/v1/track?token="

def send(url, headers, body):
    return 200  # stand-in for the real HTTP call

def fetch(url):
    raise TimeoutError(f"no reply from {url}")

def notify(order_id):
    token = os.environ["CARRIER_TOKEN"]
    headers = {"Authorization": f"Bearer {token}"}
    log.debug("headers=%s", headers)  # 2 a.m. debug line
    status = send(API, headers, {"order": order_id})
    log.info("order %s sent: %s", order_id, status)

def track(order_id):
    try:
        fetch(TRACK + os.environ["CARRIER_TOKEN"])
    except TimeoutError:
        log.exception("tracking %s failed", order_id)

if __name__ == "__main__":
    setup()
    track("A-1042")
