# Context managers for deploy scripts

Video: (link added after upload)

Needs Python 3.10 or newer. No extra packages.

## Run it

    python main.py

This walks through the whole story from the video:

1. A deploy script writes a lock file before it starts and deletes it
   when it's done, so two deploys can't collide. A real crash (a
   registry push that times out) happens between creating the lock and
   deleting it, so the delete never runs.
2. The next attempt is blocked immediately. Nothing is actually
   running, but the script can't tell the difference between a real
   deploy and a lock file nobody cleaned up.
3. The manual fix (`try`/`finally`) works for one resource, but a
   second resource (a temp build workspace) needs its own `try`/`finally`,
   and they nest awkwardly as more resources are added.
4. The real fix: turn each resource into a `@contextmanager` function
   and stack them with `with a(), b():`. Each one's cleanup runs no
   matter how the block exits, and stacking nests the cleanup in the
   right order automatically.

## Real-world anchor

The lock-file bug in this video is a fictionalized version of a real
incident: a deploy script that got killed mid-run left a lock file
behind, and it blocked every later run until someone found and
deleted it by hand. The company name and exact code are invented; the
failure mode is real.

## Limits

The "crash" (a registry timeout) and the "disk full" scenario from the
video are both simulated with a raised exception, not a real flaky
registry or a full disk. Everything else -- the lock file, the
temp workspace, the context managers -- is real and runs as shown.
