# Timeouts: why your deploy hangs forever

Video: (link added after upload)

Needs Python 3.10 or newer. No extra packages.

## Run it

    python main_before.py

fleetops' dispatch service calls the routing service's health check and
its ETA lookup, both through plain `http.client.HTTPConnection` with no
timeout set. A local TCP server stands in for a dead routing service: it
accepts the connection (it's alive) but never replies. Both calls hang
forever in real life -- capped at 3 seconds here only so the demo
finishes; the on-screen comment says so.

    python main_half_fix.py

The common half-fix: `timeout=1.5` added to the health check only. The
health check now fails fast and looks fixed. `get_eta()` -- the call
every real driver assignment depends on -- still has no timeout.

    python main_half_fix_pool.py

Same half-fix, run against fleetops' real worker pool: 4 workers, 5
dispatch jobs, all calling the still-unfixed `get_eta()`. Takes about
6.3 seconds to fail all 5 -- the pool backs up because the "fixed"
health check never touched the actual problem.

    python main.py

The real fix: one shared `call_routing()` helper with one timeout, used
by both the health check and `get_eta()`. Same load test: about 3.3
seconds instead of 6.3, nothing backs up.

## What the video covers

1. A dependency that hangs (accepts the connection, never replies) is
   worse than one that errors -- without a timeout, the caller waits
   forever. Verified live: the buggy demo actually hangs, capped only
   for the recording.
2. Adding a timeout to the one call you're staring at (the health
   check) isn't the fix if another call to the same dependency
   (`get_eta`) still has none.
3. That missed call shows up as pool exhaustion under load: 4 workers,
   5 jobs, all stuck waiting -- real numbers from a real
   `ThreadPoolExecutor`, not invented ones.
4. The real fix is one shared call path with one timeout, so nothing
   downstream of a dependency can forget to set it.
5. A timeout doesn't bring the dependency back -- it stops the blast
   radius. Two theory asides cover why this generalizes: most HTTP
   libraries default to no timeout, and a retry without a timeout just
   hangs twice.

## Real-world anchor

The cold-open incident (a dead downstream dependency with no timeout
hangs health checks and exhausts a worker pool, hiding the real outage
behind "everything looks slow") is a fictionalized version of a public
incident writeup from Val Town. No real company names, code, or
screenshots are used.

## Limits

`start_dead_routing_svc()` is a real local TCP server, not a real
second service -- but it behaves exactly like one from the caller's
side: it accepts the connection and never replies. Everything else --
the hang, the timeouts, the pool exhaustion, the fix, the timing
numbers -- is real and runs as shown.
