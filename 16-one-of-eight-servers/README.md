# Your deploy said "complete". Did all 8 servers get the new code?

Video: (link added after upload)
Shorts: (links added after upload)

> **Safety note.** Everything runs in 8 local Docker containers on your own
> PC (ports 8081 to 8088). It does not touch any real system. `send_orders.sh`
> on the old code is capped at 5000 so your laptop survives. The demo is my
> own recreation. It is **not** Knight Capital's code. The US regulator's
> order does not say how Knight copied its code, so this repo does not claim to.

Knight Capital facts come from the SEC order (Release No. 70694, 16 Oct 2013):
https://www.sec.gov/files/litigation/admin/2013/34-70694.pdf
and press release 2013-222:
https://www.sec.gov/newsroom/press-releases/2013-222

Tested with Docker 29.8.0 and the `python:3.11-slim` image on Windows 11
(Git Bash), 2026-10-17. Names are fictional (orders-router, server-1 to 8).

## Run it

You need Docker running and a bash shell (Git Bash on Windows).

    export MSYS_NO_PATHCONV=1      # Git Bash only: keeps /app paths
    ./setup.sh                     # 8 servers, all on version one
    ./versions.sh                  # server-1 to server-8: v1
    ./deploy.sh                    # copies orders_v2.py. prints "Deploy complete."
    ./versions.sh                  # server-8 is still v1: its file is read-only
    ./send_orders.sh fast          # server-8 sends 5000 orders (old meaning)
    ./check.sh v2; echo "exit code: $?"   # MISMATCH, exit code 1
    ./deploy.sh orders_v3.py       # new switch name, old code deleted
    ./send_orders.sh fast_lane     # server-8 still old, ignores the new name
    ./stop-all.sh                  # the stop button

`bash capture.sh` runs the whole sequence and writes `real_run_log.txt`.
Clean up with:

    docker rm -f server-1 server-2 server-3 server-4 server-5 server-6 server-7 server-8
    docker rmi orders-router

## The three fixes

1. `check.sh` asks every server for its version and fails (exit 1) if one differs.
2. Never give an old switch a new meaning. `orders_v3.py` uses `fast_lane` and deletes the old code.
3. `stop-all.sh` is the stop button. Try it before you need it.

## real_output

`real_output/real_run_log.txt` is the real output from my run. My other
containers in the last `docker ps` are hidden.
