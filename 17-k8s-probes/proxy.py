# proxy.py: the helper that runs next to the app
import socket, time

# wait until the old database answers
while True:
    try:
        socket.create_connection(("old-db", 5432), timeout=3)
        break
    except OSError:
        time.sleep(2)  # stay alive, keep waiting

# now open my own port, so I can say "Ready"
srv = socket.socket()
srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv.bind(("0.0.0.0", 5433))
srv.listen()
while True:
    conn, _ = srv.accept()
    conn.close()
