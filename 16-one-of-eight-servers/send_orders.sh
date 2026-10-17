#!/bin/bash
# send_orders.sh SWITCH: send one request to each server
sw=${1:-fast}
for n in 1 2 3 4 5 6 7 8; do
  echo "server-$n  $(curl -s -X POST localhost:808$n/order \
    -d "{\"item\":\"book\",\"$sw\":true}")"
done
