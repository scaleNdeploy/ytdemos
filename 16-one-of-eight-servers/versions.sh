#!/bin/bash
# versions.sh: ask every server which version it runs
for n in 1 2 3 4 5 6 7 8; do
  echo "server-$n  $(curl -s localhost:808$n/version)"
done
