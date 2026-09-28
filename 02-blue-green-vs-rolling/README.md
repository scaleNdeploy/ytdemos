# Blue-green vs rolling deploys: why requests still fail

Video: https://youtu.be/qkheQMRVmzg
Short: not uploaded yet

Needs Python 3.10 or newer. No other packages. Everything here runs real
local HTTP servers on 127.0.0.1 (no Docker, no Kubernetes, no cloud).

## Run it

Naive rolling deploy (old server is killed the instant the new one is added):

    python naive.py

Naive blue-green deploy (same problem, whole old fleet swapped at once):

    python naive_bg.py

The fix: both deploy styles, but draining connections before killing the
old server:

    python main.py

Each prints how many of the requests made during the deploy succeeded vs
failed, for example:

    rolling, naive     ok  148  failed   32
    blue-green, naive  ok  161  failed   19
    rolling, safe      ok  180  failed    0
    blue-green, safe   ok  180  failed    0

## What this shows

A small pool of Python HTTP servers behind a simple round-robin load
balancer. During a deploy, old servers are swapped for new ones. If the
old server is killed immediately, requests already sent to it fail. If
you drain it first (stop sending it new requests, wait for in-flight
ones to finish, then kill it), nothing fails, whether you deploy one
server at a time (rolling) or the whole fleet at once (blue-green).

## Limits

This is a local simulation with Python's built-in `http.server`, not a
real cluster. Timings (boot time, request duration, drain time) are
fixed constants picked to make the effect visible in a short run, not
measured from a real system. Real load balancers, real Kubernetes
rolling updates, and real blue-green setups (behind a real load
balancer or DNS switch) have more moving parts than shown here, but the
core idea, drain before you kill, is the same one they rely on.
