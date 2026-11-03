#!/bin/bash
# restore-test.sh: restore the latest backup into a scratch
# database, then compare the row count with the live one
set -e
PSQL="docker exec -i orders-db psql -U demo -tA"
docker exec orders-db createdb -U demo restore_check
$PSQL -q restore_check < backups/orders.sql
live=$($PSQL orders -c "SELECT count(*) FROM orders")
got=$($PSQL restore_check -c "SELECT count(*) FROM orders")
docker exec orders-db dropdb -U demo restore_check
if [ "$live" = "$got" ]; then
  echo "RESTORE OK: $got rows"
else
  echo "RESTORE FAILED: live $live, restored $got"
  exit 1
fi
