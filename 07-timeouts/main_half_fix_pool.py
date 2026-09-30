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


def _demo_cap(fn, seconds=3):
    # DEMO ONLY: caps a hang so this recording
    # finishes.
    out = {}

    def run():
        out["v"] = fn()

    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(timeout=seconds)
    if t.is_alive():
        return "TIMED OUT (demo cap)"
    return out.get("v")


def check_routing_health():
    # FIXED: timeout=1.5
    try:
        conn = http.client.HTTPConnection(
            "127.0.0.1", ROUTING_PORT,
            timeout=1.5)
        conn.request("GET", "/health")
        return conn.getresponse().status == 200
    except OSError:
        return False


def get_eta(job_id):
    # still BUG: no timeout -- same call every real
    # driver assignment depends on
    conn = http.client.HTTPConnection(
        "127.0.0.1", ROUTING_PORT)
    conn.request("GET", f"/eta?job={job_id}")
    return conn.getresponse().status == 200


def run_dispatch_load():
    # fleetops' worker pool: 4 workers, shared by
    # health checks and real dispatch jobs
    with Pool(max_workers=4) as pool:
        futs = {
            pool.submit(
                _demo_cap, lambda j=j: get_eta(j)
            ): j
            for j in JOBS
        }
        for fut in futs:
            job = futs[fut]
            print(job, "eta ok:", fut.result())


if __name__ == "__main__":
    threading.Thread(
        target=start_dead_routing_svc,
        args=(ROUTING_PORT,), daemon=True).start()
    time.sleep(0.2)
    run_dispatch_load()
