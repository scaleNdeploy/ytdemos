#!/bin/bash
# capture.sh: runs the whole demo and writes REAL output to
# real_run_log.txt. Run it from this folder in Git Bash:
#     bash capture.sh
# Needs Docker Desktop running. Uses only local containers.
export MSYS_NO_PATHCONV=1   # Git Bash on Windows: keep /app paths
cd "$(dirname "$0")" || exit 1
log=real_run_log.txt
: > $log

# stop if something already uses ports 8081 to 8088
for n in 1 2 3 4 5 6 7 8; do
  if curl -s -m 1 localhost:808$n > /dev/null 2>&1; then
    echo "Port 808$n is already in use. Stop and tell Claude."; exit 1
  fi
done

run() {
  printf '$ %s\n' "$1" >> $log
  eval "$1" >> $log 2>&1
  echo >> $log
}

# make sure old containers from an earlier try are gone
docker rm -f server-1 server-2 server-3 server-4 server-5 \
  server-6 server-7 server-8 > /dev/null 2>&1

run 'docker --version'
run './setup.sh'
sleep 3
run './versions.sh'
run './deploy.sh'
run './versions.sh'
run './send_orders.sh fast'
run './check.sh v2; echo "exit code: $?"'
run './deploy.sh orders_v3.py'
run './send_orders.sh fast_lane'
run './stop-all.sh'
run 'docker ps'

# clean up
docker rm -f server-1 server-2 server-3 server-4 server-5 \
  server-6 server-7 server-8 > /dev/null 2>&1
docker rmi orders-router > /dev/null 2>&1
echo "Done. Output is in $log"
