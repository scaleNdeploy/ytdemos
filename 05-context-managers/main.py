"""lattice's deploy script: a real crash-then-blocked-retry story, and the
context-manager fix. Fictional company; the story is real (a lesson from
production): a deploy script crashed mid-run, left a lock file behind, and
blocked every later run until someone found and deleted it by hand."""
import os
import shutil
import tempfile
from contextlib import contextmanager

LOCK_FILE = ".deploy.lock"


# ---------------------------------------------------------------- the bug

def deploy_buggy():
    """Writes a lock file before starting, deletes it when done. If the
    lock file already exists, refuses to start -- meant to stop two
    deploys from colliding."""
    if os.path.exists(LOCK_FILE):
        raise SystemExit("another deploy is already running")
    open(LOCK_FILE, "w").close()
    run_steps_buggy()
    os.remove(LOCK_FILE)


def run_steps_buggy():
    print("building release...")
    print("pushing to registry...")
    push_to_registry()
    print("restarting service...")


def push_to_registry():
    raise ConnectionError("registry timed out (simulated)")


def run_buggy_demo():
    print("-- first run: a real crash, simulated here --")
    try:
        deploy_buggy()
    except SystemExit as err:
        print(f"blocked: {err}")
    except Exception as err:
        print(f"deploy failed: {err}")
    print("lock file present:", os.path.exists(LOCK_FILE))

    print()
    print("-- retry the next day: nothing is actually running --")
    try:
        deploy_buggy()
    except SystemExit as err:
        print(f"blocked: {err}")
    except Exception as err:
        print(f"deploy failed: {err}")
    print("lock file present:", os.path.exists(LOCK_FILE))


# ---------------------------------------------------------------- the fix

@contextmanager
def deploy_lock():
    """The lock, as a context manager. The `finally` runs no matter how
    the `with` block exits: a clean finish, an exception, anything."""
    if os.path.exists(LOCK_FILE):
        raise SystemExit("another deploy is already running")
    open(LOCK_FILE, "w").close()
    try:
        yield
    finally:
        os.remove(LOCK_FILE)


@contextmanager
def build_workspace():
    """A second resource, cleaned up the same guaranteed way. Stacking
    `with` statements nests the cleanup: build_workspace's `finally` runs
    before deploy_lock's, in the reverse order they were entered."""
    print("checking disk space...")
    workdir = tempfile.mkdtemp()
    try:
        yield workdir
    finally:
        shutil.rmtree(workdir)


def deploy_fixed():
    with deploy_lock(), build_workspace() as workdir:
        run_steps_fixed(workdir)


def run_steps_fixed(workdir):
    print("building release in", os.path.basename(workdir))
    print("pushing to registry...")
    print("restarting service...")


def run_fixed_demo():
    print("-- fixed version: two context managers, stacked --")
    deploy_fixed()
    print("lock file present:", os.path.exists(LOCK_FILE))
    print()
    print("-- run it again right away: no leftover lock, no problem --")
    deploy_fixed()
    print("lock file present:", os.path.exists(LOCK_FILE))


if __name__ == "__main__":
    run_buggy_demo()
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)  # cleaning up by hand -- the old, manual fix
    print()
    run_fixed_demo()
