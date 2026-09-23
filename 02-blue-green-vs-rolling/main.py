import itertools, threading, time, urllib.request
import http.server as hs

BOOT, LAG, WORK, END, RATE = 1.0, 0.5, 0.3, 9, 20
ports = itertools.count(9100)
lock = threading.Lock()
count = {"ok": 0, "bad": 0}

class Server:
    def __init__(self):
        self.port = next(ports)
        self.ready = self.dead = False

    def boot(self, delay):
        time.sleep(delay)
        me = self

        class Handler(hs.BaseHTTPRequestHandler):
            def do_GET(self):
                time.sleep(WORK)
                if me.dead:
                    return
                self.send_response(200)
                self.end_headers()
                self.wfile.write(b"ok")

            def log_message(self, *args):
                pass

        addr = ("127.0.0.1", self.port)
        self.http = hs.ThreadingHTTPServer(addr, Handler)
        threading.Thread(target=self.http.serve_forever,
                         daemon=True).start()
        self.ready = True

    def stop(self, drain):
        time.sleep(drain)
        self.dead = True
        self.http.shutdown()
        self.http.server_close()

class Balancer:
    def __init__(self, servers):
        self.pool = list(servers)
        self.turn = itertools.count()

    def add(self, s):
        self.pool.append(s)

    def remove(self, s):
        t = threading.Timer(LAG, self.pool.remove, [s])
        t.daemon = True
        t.start()

    def get(self):
        pool = list(self.pool)
        s = pool[next(self.turn) % len(pool)]
        try:
            url = f"http://127.0.0.1:{s.port}/"
            urllib.request.urlopen(url, timeout=3).read()
            key = "ok"
        except Exception:
            key = "bad"
        with lock:
            count[key] += 1

def swap(lb, old, safe):
    new = Server()
    threading.Thread(target=new.boot, args=(BOOT,),
                     daemon=True).start()
    if not safe:
        lb.add(new)
    while not new.ready:
        time.sleep(0.01)
    if safe:
        lb.add(new)
    lb.remove(old)
    old.stop(LAG + WORK + 0.2 if safe else 0)

def deploy(lb, old, plan, safe):
    t0 = time.time()
    for at, i in plan:
        time.sleep(max(0, t0 + at - time.time()))
        threading.Thread(target=swap, daemon=True,
                         args=(lb, old[i], safe)).start()

def run(name, plan, safe):
    count.update(ok=0, bad=0)
    old = [Server() for _ in range(4)]
    for s in old:
        s.boot(0)
    lb = Balancer(old)
    threading.Thread(target=deploy, daemon=True,
                     args=(lb, old, plan, safe)).start()
    t0, jobs = time.time(), []
    for i in range(END * RATE):
        time.sleep(max(0, t0 + i / RATE - time.time()))
        jobs.append(threading.Thread(target=lb.get))
        jobs[-1].start()
    for j in jobs:
        j.join()
    ok, bad = count["ok"], count["bad"]
    print(f"{name:18} ok {ok:4d}  failed {bad:3d}")

rolling = [(1 + 1.5 * k, k) for k in range(4)]
bluegreen = [(1, k) for k in range(4)]
run("rolling, safe", rolling, True)
run("blue-green, safe", bluegreen, True)
