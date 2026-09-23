# Deleted the key? It is still in Git

Video: https://youtu.be/Et33NM8Gf4w
Short: not uploaded yet

Needs Python 3.10 or newer, git, and
[gitleaks](https://github.com/gitleaks/gitleaks) on your PATH.

This repo does not contain any real or static fake secrets. Every fake
AWS key, password, and SSH key is generated fresh, in memory, each time
you run the demo (see `generate_secrets.py`), inside a throwaway git
repo under your system's temp directory. Nothing here is a real
credential, and nothing here needs to be revoked.

## Run it

    python demo.py

This walks through the whole story from the video, printing each step
as it happens:
1. Commit a settings file with a fake AWS key, secret, DB password, and
   an SSH private key.
2. Scan the history with `gitleaks git . -v` and see it find all four.
3. The wrong fix: take the secrets out of the current file and commit
   that. Scanning the working files is clean, but scanning the history
   still finds the old secrets.
4. The fix that actually prevents it: a `pre-commit` git hook that runs
   gitleaks before every commit, blocking a secret before it ever
   reaches history.

## The right order (not automated here, just explained)

1. Treat any committed key as compromised: revoke it and issue a new
   one. This matters most, and rewriting history does not undo it.
2. Keep secrets out of the code (environment variables, or a secrets
   manager).
3. Rewriting history (`git filter-repo`, BFG) only cleans your own
   repo. Anyone who already cloned it still has the old key.
4. Scan before every commit, so it never gets that far. That's the
   `pre-commit` hook step above.

## Limits

The temp repo this creates is deleted automatically when the script
finishes. `gitleaks` is a real, third-party tool; install it yourself
from its GitHub releases. This script assumes it is already on your
PATH.
