# Your backup says "complete". Is the file empty?

Video: [add after upload]
Shorts: [add after upload]

> **Safety note.** Everything runs in one local Docker container
> (`orders-db`) with 200 fake rows. It does not touch any real system.
> The demo is my own recreation. It is **not** GitLab's setup. GitLab's
> postmortem does not name the exact command or the engineer, so this
> repo does not claim either.

GitLab facts come from GitLab's own postmortem (31 Jan 2017):
https://about.gitlab.com/blog/postmortem-of-database-outage-of-january-31/
Dump tool and server versions: https://www.postgresql.org/docs/current/app-pgdump.html

The password `demo` belongs to a throwaway local container with fake data. It is not a real secret.

Tested with Docker 29.8.0, Postgres 16.13 (server) and Postgres 15.13
(the older dump tool) on Windows 11 (Git Bash), 2026-11-03.
Names are fictional (orders-db, orders table).

## Run it

You need Docker running and a bash shell (Git Bash on Windows).
The first run pulls `postgres:16` and `postgres:15` (small official images).

    export MSYS_NO_PATHCONV=1                 # Git Bash only
    bash setup.sh                             # Postgres 16 + 200 fake orders
    ./backup.sh                               # prints "Backup complete."
    wc -c backups/orders.sql                  # 0 bytes
    cat backup.log                            # the hidden version mismatch
    bash seed.sh; rm -rf backups backup.log   # start over
    ./backup-checked.sh                       # fix 1: FAILED, loudly
    ./backup-fixed.sh                         # fix 2: right tool, real size
    ./restore-test.sh                         # fix 3: RESTORE OK: 200 rows

`bash capture.sh` runs the whole sequence and writes `real_run_log.txt`.
Clean up with:

    docker rm -f orders-db
    docker rmi postgres:15      # optional

## The three fixes

1. `backup-checked.sh` checks the result of the dump and fails loudly.
2. `backup-fixed.sh` dumps with the database's own tool (same version) and refuses an empty file.
3. `restore-test.sh` restores the latest backup into a scratch database and compares the row count with the live one. Run it every night and make it shout when it fails.

## real_output

`real_output/real_run_log.txt` is the real output from my run.
