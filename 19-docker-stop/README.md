# Why docker stop takes 10 seconds (and the one line that fixes it)

Video: [add after upload]
Short: [add after upload]

> **Safety note.** Everything runs in local Docker containers with a
> tiny fake worker (`payments-api`). It does not touch any real system.

How it works: `docker stop` sends a stop message (SIGTERM), waits, then
kills the container (SIGKILL). If a shell sits in front of your app
(shell form `CMD python worker.py`), the shell may not pass the message
on. The exec form `CMD ["python", "worker.py"]` starts the app directly.

Docker docs:
- https://docs.docker.com/reference/cli/docker/container/stop/
- https://docs.docker.com/reference/build-checks/json-args-recommended/

Tested with Docker 29.8.0 (Docker Desktop, WSL2), `python:3.11-slim`,
Windows 11 (Git Bash), 2026-11-09. Names are fictional.

**About the wait time.** Docker's docs say the default stop timeout is
10 seconds on Linux (30 on Windows). On my Docker Desktop it was about
3 seconds (my own measurement, see `real_output/diag_log.txt`). So the
slow cases use `docker stop -t 10` to match a Linux server.

## Run it

You need Docker running and a bash shell (Git Bash on Windows).
The first run pulls `python:3.11-slim` (a small official image).

    export MSYS_NO_PATHCONV=1                 # Git Bash only
    docker build -f Dockerfile.slow -t worker:slow .
    docker build -f Dockerfile.fast -t worker:fast .
    docker run -d --name worker-slow worker:slow
    docker top worker-slow                    # a shell, then the app
    time docker stop -t 10 worker-slow        # about 10 s, then killed
    docker inspect -f "{{.State.ExitCode}}" worker-slow   # 137
    docker run -d --name worker-fast worker:fast
    time docker stop worker-fast              # about 1 s
    docker inspect -f "{{.State.ExitCode}}" worker-fast   # 0

`bash capture.sh` runs the whole sequence and writes `real_run_log.txt`.
Clean up with:

    docker rm -f worker-slow worker-fast worker-nohandler worker-init

## Files

- `worker.py`: tiny order worker that handles the stop message
- `Dockerfile.slow`: shell form CMD
- `Dockerfile.fast`: exec form CMD (square brackets)
- `worker-nohandler.py`, `Dockerfile.nohandler`: an app with no stop
  handler (used by `capture.sh`; the topic of the next video)
- `diag.sh`: how I measured the Docker Desktop default

## real_output

`real_output/real_run_log.txt` is the real output from my run.
