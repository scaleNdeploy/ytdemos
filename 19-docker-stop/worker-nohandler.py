import time

order = 0
print("worker started", flush=True)
while True:
    order += 1
    print(f"processing order {order}", flush=True)
    time.sleep(0.5)
