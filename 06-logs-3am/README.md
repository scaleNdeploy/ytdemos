# Logs you can read at 3AM

Video: (link added after upload)

Needs Python 3.10 or newer. No extra packages.

## Run it

    python main_before.py

This is the "before" version: five orders come in at the same time,
logged with plain `print()`. One customer was charged twice (order
`O-1003`) -- see if you can spot it in the output.

    python main.py

This is the fixed version: structured (JSON) logs, a `contextvars.ContextVar`
holding a per-request ID set once when a request starts and read by every
log call after that, and a second file, `payments.py`, standing in for a
second service that the first one calls. The ID is passed across that call
as a header and set again on the receiving side -- both "services" run in
this one process for the demo, but the pattern (pass it, then set it again)
is exactly what you'd do for two real services.

Filter to one request across both services:

    python main.py | grep req-O-1003

## What the video covers

1. `print()` statements interleave into an unreadable mess once requests
   run concurrently -- a real bug (a duplicate charge) is in there, but
   good luck finding it by eye.
2. Structured logs plus a context variable fix this inside one process --
   verified for real: `asyncio.Task` correctly copies context per task,
   so concurrent requests never leak IDs into each other.
3. A common half-finished version of the fix: structured logging is added,
   but nothing ever calls `.set()`, so every line still shows the same
   default ID. One missing line, shown live.
4. The same idea has to be repeated at every service boundary: a
   context variable does not cross a network call by itself. Pass it
   explicitly (a header, here), and set it again on the other side.

## Real-world anchor

The cold-open incident in the video (dashboards look healthy while one
customer's request is actually broken, found only after digging through
a wall of text logs) is a fictionalized composite of three real, public
sources: GitLab's own writeups on request-correlation (Ray-ID) logging,
Monzo's 2019 outage postmortem, and Uber's public writeup on why they
built distributed tracing. No single incident matches this story exactly
-- it's a synthesis, not a retelling of one event.

## Limits

`payments.py` is a second file, not a second process -- there is no real
network call here, just a plain function call standing in for one. The
pattern (pass the ID as a header, set it again on the receiving side) is
what you'd actually do across a real network boundary. Everything else --
the concurrency, the bug, the logs, the fix -- is real and runs as shown.
