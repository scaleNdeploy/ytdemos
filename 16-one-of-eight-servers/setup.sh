#!/bin/bash
# setup.sh: start 8 servers, all on version one
docker build -q -t orders-router .
for n in 1 2 3 4 5 6 7; do
  docker run -d --name server-$n -p 808$n:8000 orders-router
done
# server 8: its code file is locked (read-only)
docker run -d --name server-8 -p 8088:8000 \
  -v "$PWD/orders_v1.py:/app/orders.py:ro" orders-router
