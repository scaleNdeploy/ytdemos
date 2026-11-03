#!/bin/bash
# capture.sh: runs the whole demo and writes REAL output to
# real_run_log.txt. Run it from this folder in Git Bash:
#     bash capture.sh
# Needs Docker Desktop running. Uses minikube (a local cluster).
export MSYS_NO_PATHCONV=1
cd "$(dirname "$0")" || exit 1
log=real_run_log.txt
: > $log

run() {
  printf '$ %s\n' "$1" >> $log
  eval "$1" >> $log 2>&1
  echo >> $log
}

# a cluster must be running. This may download an image once.
if ! kubectl get nodes > /dev/null 2>&1; then
  minikube start --driver=docker || { echo "minikube did not start"; exit 1; }
fi
kubectl config use-context minikube > /dev/null 2>&1

# clean start
kubectl delete deployment orders-api old-db --ignore-not-found > /dev/null 2>&1
kubectl delete service orders-api old-db --ignore-not-found > /dev/null 2>&1
kubectl delete configmap proxy-code --ignore-not-found > /dev/null 2>&1

run 'kubectl version --client'
run 'kubectl create configmap proxy-code --from-file=proxy.py'
run 'kubectl apply -f old-db.yaml'
kubectl wait --for=condition=Available deployment/old-db --timeout=180s > /dev/null 2>&1
run 'kubectl apply -f deployment.yaml'
kubectl wait --for=condition=Ready pod -l app=orders-api --timeout=180s > /dev/null 2>&1
sleep 5
run 'kubectl get pods -l app=orders-api'
run 'grep -n old-db proxy.py deployment.yaml'
run 'kubectl delete -f old-db.yaml'
sleep 15
run 'kubectl get pods -l app=orders-api'
run 'kubectl scale deployment orders-api --replicas=4'
sleep 40
run 'kubectl get pods -l app=orders-api'
run 'kubectl describe pods -l app=orders-api | grep -m3 "5433"'
run 'kubectl get endpoints orders-api'
run 'kubectl apply -f deployment-fixed.yaml'
kubectl rollout status deployment/orders-api --timeout=180s > /dev/null 2>&1
sleep 35
run 'kubectl get pods -l app=orders-api'
run 'kubectl apply -f deployment-liveness.yaml'
sleep 120
run 'kubectl get pods -l app=orders-api'

# clean up (the cluster keeps running; stop it with: minikube stop)
kubectl delete deployment orders-api old-db --ignore-not-found > /dev/null 2>&1
kubectl delete service orders-api old-db --ignore-not-found > /dev/null 2>&1
kubectl delete configmap proxy-code --ignore-not-found > /dev/null 2>&1
echo "Done. Output is in $log"
