import http.client
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor as Pool

ROUTING_PORT = 8765
JOBS = ["D-201", "D-202", "D-203", "D-204", "D-205"]


def start_dead_routing_svc(port):
    conns = []
    srv = socket.socket(
        socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(
        socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind(("127.0.0.1", port))
    srv.listen(16)
    while True:
        conn, _ = srv.accept()
        conns.append(conn)


def call_routing(path, timeout=1.5):
    # FIX: one shared call, one shared timeout --
    # every outbound call to routing-svc goes
    # through here now
    try:
        conn = http.client.HTTPConnection(
            "127.0.0.1", ROUTING_PORT,
            timeout=timeout)
        conn.request("GET", path)
        return conn.getresponse().status == 200
    except OSError:
        return False


def check_routing_health():
    return call_routing("/health")


def get_eta(job_id):
    return call_routing(f"/eta?job={job_id}")


def run_dispatch_load():
    # same four workers, same five jobs
    with Pool(max_workers=4) as pool:
        futs = {pool.submit(get_eta, j): j
                for j in JOBS}
        for fut in futs:
            job = futs[fut]
            print(job, "eta ok:", fut.result())


if __name__ == "__main__":
    threading.Thread(
        target=start_dead_routing_svc,
        args=(ROUTING_PORT,), daemon=True).start()
    time.sleep(0.2)
    run_dispatch_load()
