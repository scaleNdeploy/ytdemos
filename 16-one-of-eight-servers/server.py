# server.py: the same web server on all 8 servers.
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

import orders

total = 0


class Handler(BaseHTTPRequestHandler):
    def _reply(self, text):
        data = text.encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/version":
            self._reply(orders.VERSION)
        elif self.path == "/stats":
            self._reply(json.dumps({"sent": total}))
        else:
            self.send_error(404)

    def do_POST(self):
        global total
        size = int(self.headers.get("Content-Length", 0))
        order = json.loads(self.rfile.read(size) or b"{}")
        sent, lane = orders.handle(order)
        total += sent
        self._reply(json.dumps({"sent": sent, "lane": lane}))

    def log_message(self, *args):
        pass


HTTPServer(("0.0.0.0", 8000), Handler).serve_forever()
