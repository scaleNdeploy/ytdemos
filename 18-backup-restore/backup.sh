#!/bin/bash
# backup.sh: nightly backup of the orders database
mkdir -p backups
docker run --rm --network container:orders-db \
  -e PGPASSWORD=demo postgres:15 \
  pg_dump -h localhost -U demo orders \
  > backups/orders.sql 2>> backup.log
echo "Backup complete."
