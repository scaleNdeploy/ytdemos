#!/bin/bash
# backup-fixed.sh: the database's own tool, then a check
mkdir -p backups
docker exec orders-db pg_dump -U demo orders \
  > backups/orders.tmp 2>> backup.log
if [ ! -s backups/orders.tmp ]; then
  echo "FAILED: the backup file is empty"
  exit 1
fi
mv backups/orders.tmp backups/orders.sql
echo "Backup complete: $(wc -c < backups/orders.sql) bytes"
