#!/bin/bash
# capture.sh: runs the whole demo and writes REAL output to
# real_run_log.txt. Run it from this folder in Git Bash:
#     bash capture.sh
# Needs Docker Desktop running. Pulls python:3.11-slim (small).
export MSYS_NO_PATHCONV=1
cd "$(dirname "$0")" || exit 1
log=real_run_log.txt
: > $log
TIMEFORMAT=$'real\t%1lR'

run() {
  printf '$ %s\n' "$1" >> $log
  eval "$1" >> $log 2>&1
  echo >> $log
}

# clean start
docker rm -f worker-slow worker-fast worker-nohandler \
  worker-init > /dev/null 2>&1

docker build -q -f Dockerfile.slow -t worker:slow . > /dev/null
docker build -q -f Dockerfile.fast -t worker:fast . > /dev/null
docker build -q -f Dockerfile.nohandler -t worker:nohandler . \
  > /dev/null

run 'docker --version'
run 'docker run --rm python:3.11-slim python --version'

# Docker Desktop on this PC gives up after about 3 s (see diag_log.txt).
# Docs say the Linux default is 10 s, so the slow cases use -t 10.

# 1. shell form: slow
run 'docker run -d --name worker-slow worker:slow'
sleep 3
run 'docker top worker-slow'
run 'time docker stop -t 10 worker-slow'
run 'docker inspect -f "{{.State.ExitCode}}" worker-slow'
run 'docker logs --tail 3 worker-slow'

# 2. exec form: fast
run 'docker run -d --name worker-fast worker:fast'
sleep 3
run 'docker top worker-fast'
run 'time docker stop worker-fast'
run 'docker inspect -f "{{.State.ExitCode}}" worker-fast'
run 'docker logs --tail 3 worker-fast'

# 3. exec form, but no signal handler: slow again
run 'docker run -d --name worker-nohandler worker:nohandler'
sleep 3
run 'time docker stop -t 10 worker-nohandler'
run 'docker inspect -f "{{.State.ExitCode}}" worker-nohandler'
run 'docker logs --tail 3 worker-nohandler'

# 4. the shortcut that is not a fix: a 1 second timeout
docker rm -f worker-slow > /dev/null 2>&1
run 'docker run -d --name worker-slow worker:slow'
sleep 3
run 'time docker stop -t 1 worker-slow'
run 'docker inspect -f "{{.State.ExitCode}}" worker-slow'
run 'docker logs --tail 3 worker-slow'

# 5. bonus check (shown only if it works): --init
run 'docker run -d --init --name worker-init worker:nohandler'
sleep 3
run 'time docker stop worker-init'
run 'docker inspect -f "{{.State.ExitCode}}" worker-init'

# clean up
docker rm -f worker-slow worker-fast worker-nohandler \
  worker-init > /dev/null 2>&1
echo "Done. Output is in $log"
