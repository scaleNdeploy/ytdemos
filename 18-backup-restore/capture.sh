#!/bin/bash
# capture.sh: runs the whole demo and writes REAL output to
# real_run_log.txt. Run it from this folder in Git Bash:
#     bash capture.sh
# Needs Docker Desktop running. Pulls postgres:16 and postgres:15
# once (small official images).
export MSYS_NO_PATHCONV=1
cd "$(dirname "$0")" || exit 1
log=real_run_log.txt
: > $log
rm -rf backups backup.log

run() {
  printf '$ %s\n' "$1" >> $log
  eval "$1" >> $log 2>&1
  echo >> $log
}

bash setup.sh
run 'docker --version'
run 'docker exec orders-db psql --version'
run 'docker exec orders-db psql -U demo orders -c "SELECT count(*) FROM orders"'
run './backup.sh'
run 'wc -c backups/orders.sql'
run 'cat backup.log'
run 'docker exec orders-db psql -U demo orders -c "DROP TABLE orders"'
run 'docker exec -i orders-db psql -U demo orders < backups/orders.sql'
run 'docker exec orders-db psql -U demo orders -c "SELECT count(*) FROM orders"'

# start over on a fresh table (not shown as a step)
bash seed.sh
rm -rf backups backup.log
run './backup-checked.sh'
run './backup-fixed.sh'
run 'wc -c backups/orders.sql'
run './restore-test.sh'

# clean up
docker rm -f orders-db > /dev/null 2>&1
echo "Done. Output is in $log"
