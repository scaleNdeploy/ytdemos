import http.client
import socket
import threading
import time

ROUTING_PORT = 8765


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


def check_routing_health():
    # FIXED: timeout=1.5, and catch it
    try:
        conn = http.client.HTTPConnection(
            "127.0.0.1", ROUTING_PORT,
            timeout=1.5)
        conn.request("GET", "/health")
        return conn.getresponse().status == 200
    except OSError:
        return False


def get_eta(job_id):
    # still BUG: no timeout
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
    print("healthy:", check_routing_health())
