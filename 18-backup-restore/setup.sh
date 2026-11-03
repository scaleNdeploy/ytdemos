#!/bin/bash
# setup.sh: a small Postgres 16 in Docker, with 200 fake orders
export MSYS_NO_PATHCONV=1
docker rm -f orders-db > /dev/null 2>&1
docker run -d --name orders-db \
  -e POSTGRES_USER=demo -e POSTGRES_PASSWORD=demo \
  -e POSTGRES_DB=orders postgres:16 > /dev/null
until docker exec orders-db pg_isready -U demo -d orders \
  > /dev/null 2>&1; do sleep 1; done
sleep 2
bash seed.sh
