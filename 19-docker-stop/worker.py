import signal
import time

stopping = False


def on_stop(signum, frame):
    global stopping
    stopping = True
    print("got SIGTERM, finishing", flush=True)


signal.signal(signal.SIGTERM, on_stop)

order = 0
print("worker started", flush=True)
while not stopping:
    order += 1
    print(f"processing order {order}", flush=True)
    time.sleep(0.5)
print(f"order {order} done, bye", flush=True)
