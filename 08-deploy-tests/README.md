# Test your deploy script without deploying

Video: (link added after upload)

Needs Python 3.10 or newer and pytest (`pip install pytest`).

## Run it

    python3 deploy_before.py

flowdesk's deploy script pushes code to three servers over `ssh_connect`
(a stand-in for a real SSH connection -- `srv-2` is always down, the way
one real server was during a real 2012 trading-firm deploy). It prints a
warning for the dead server, then returns `True` no matter what happened.

    python3 -m pytest test_deploy_before.py -v

A test that fakes the connection so `srv-2` always fails. It checks only
the one thing a caller actually sees: the return value. Fails immediately,
with no real server anywhere near it.

    python3 deploy_half_fix.py
    python3 -m pytest test_deploy_half_fix.py -v

The obvious next step: print a clearer warning when a server fails. The
test still fails -- a clearer warning isn't the same as reporting failure,
and the return value, the only thing a caller checks, is still `True`.

    python3 deploy.py
    python3 -m pytest test_deploy.py -v

The real fix: track every failure and return `len(failures) == 0`. Test
passes, and `deploy.py` now prints `deploy successful: False` for real.

## What the video covers

1. A deploy script that swallows a connection error can still report
   success -- the caller never sees the warning, only the return value.
2. Mock the dependency you can't safely touch in a test (the SSH
   connection), not the logic you're actually testing.
3. A clearer warning isn't the same as reporting failure. If the return
   value doesn't change, the bug is still there.
4. Fast mocked tests catch this kind of logic bug on every commit, without
   a real server anywhere nearby.
5. What this doesn't prove: a mocked test proves the deploy script's own
   logic, not that the real SSH connection or the real server works. You
   still want an occasional real staging deploy.

## Real-world anchor

The cold open (a deploy script that updates only some of the servers, and
reports success anyway because it silently swallowed a connection
failure) is a fictionalized version of the 2012 Knight Capital trading
glitch: a deploy script updated 9 of 10 production servers because it
failed to open an SSH connection to the 10th, failed silently, and
reported success. Dormant old code on that one untouched server then ran
against a reused settings flag, and Knight Capital lost $460 million in
45 minutes. Sources: U.S. Securities and Exchange Commission press
release (sec.gov/news/press-release/2013-222) and a public technical
writeup of the incident (specbranch.com). No real company names, code,
or screenshots are used -- "flowdesk" and its deploy script are fictional.

## Limits

`ssh_connect()` always fails for `srv-2` and always succeeds otherwise --
it's a stand-in for a real SSH connection, not a real one. The deploy
logic, the test, and all terminal output are real and run as shown.
