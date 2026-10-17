#!/bin/bash
# check.sh: all 8 servers must run the same version
want=${1:-v2}; bad=0
for n in 1 2 3 4 5 6 7 8; do
  got=$(curl -s localhost:808$n/version)
  echo "server-$n  $got"
  [ "$got" = "$want" ] || bad=1
done
[ $bad = 0 ] || { echo "MISMATCH. Do not go live."; exit 1; }
echo "All 8 match."
