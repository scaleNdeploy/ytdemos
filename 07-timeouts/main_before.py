import http.client
import socket
import threading
import time

ROUTING_PORT = 8765


def start_dead_routing_svc(port):
    # routing-svc: accepts the TCP connection (it IS
    # alive) but never replies -- a dependency that
    # hangs, not one that errors
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
    # finishes. fn() below is the real, unmodified
    # buggy call.
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
    # BUG: no timeout on this call
    conn = http.client.HTTPConnection(
        "127.0.0.1", ROUTING_PORT)
    conn.request("GET", "/health")
    return conn.getresponse().status == 200


def get_eta(job_id):
    # BUG: no timeout here either
    conn = http.client.HTTPConnection(
        "127.0.0.1", ROUTING_PORT)
    conn.request("GET", f"/eta?job={job_id}")
    return conn.getresponse().status == 200


if __name__ == "__main__":
    threading.Thread(
        target=start_dead_routing_svc,
        args=(ROUTING_PORT,), daemon=True).start()
    time.sleep(0.2)

    print("checking routing-svc health...")
    ok = _demo_cap(check_routing_health)
    print("healthy:", ok)

    print("assigning driver, job D-201...")
    ok = _demo_cap(lambda: get_eta("D-201"))
    print("eta ok:", ok)
