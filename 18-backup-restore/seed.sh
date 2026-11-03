#!/bin/bash
# seed.sh: (re)create the orders table with 200 fake rows
export MSYS_NO_PATHCONV=1
docker exec orders-db psql -q -U demo orders -c "
DROP TABLE IF EXISTS orders;
CREATE TABLE orders AS
  SELECT g AS id, 'order-' || g AS name, (g * 7) % 100 + 5 AS total
  FROM generate_series(1, 200) g;"
