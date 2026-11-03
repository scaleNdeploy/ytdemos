#!/bin/bash
# backup-checked.sh: same tool, but it checks the result
mkdir -p backups
if ! docker run --rm --network container:orders-db \
  -e PGPASSWORD=demo postgres:15 \
  pg_dump -h localhost -U demo orders \
  > backups/orders.sql 2>> backup.log; then
  echo "FAILED: the dump tool stopped. See backup.log"
  exit 1
fi
echo "Backup complete."
