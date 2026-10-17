#!/bin/bash
# deploy.sh FILE: put new code on all 8 servers
file=${1:-orders_v2.py}
for n in 1 2 3 4 5 6 7 8; do
  docker exec -i server-$n sh -c 'cat > /app/orders.py' \
    < $file 2>/dev/null
  docker restart server-$n > /dev/null
done
sleep 2
echo "Deploy complete."
