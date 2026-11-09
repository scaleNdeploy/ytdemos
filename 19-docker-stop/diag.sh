#!/bin/bash
# diag.sh: why did "docker stop" give up after about 3 seconds
# and not 10? Writes diag_log.txt. Run: bash diag.sh
export MSYS_NO_PATHCONV=1
cd "$(dirname "$0")" || exit 1
log=diag_log.txt
: > $log
TIMEFORMAT=$'real\t%1lR'
run() {
  printf '$ %s\n' "$1" >> $log
  eval "$1" >> $log 2>&1
  echo >> $log
}
docker rm -f worker-slow worker-fast > /dev/null 2>&1
run 'docker version --format "server {{.Server.Version}}"'
run 'docker info | grep -i -E "timeout|stop|Server Version|Operating System|Kernel Version|Context"'
run 'docker context ls'
run 'docker run -d --name worker-slow worker:slow'
sleep 3
run 'docker inspect -f "StopTimeout={{.Config.StopTimeout}} StopSignal={{.Config.StopSignal}}" worker-slow'
run 'time docker stop -t 10 worker-slow'
run 'docker inspect -f "{{.State.ExitCode}}" worker-slow'
docker rm -f worker-slow > /dev/null 2>&1
run 'docker run -d --name worker-slow worker:slow'
sleep 3
run 'time docker stop worker-slow'
docker rm -f worker-slow > /dev/null 2>&1
echo "Done. Output is in $log"
