# Why your new pods stay at 1/2 Ready (a dead helper container)

Video: https://youtu.be/leOwCJbLUeM
Shorts: https://youtube.com/shorts/W8Bki_sakR0 , https://youtube.com/shorts/u8wkOpQicSM

> **Safety note.** Everything runs on a local minikube cluster on your own
> PC. It does not touch any real system. The demo is my own recreation. It
> is **not** Expo's setup. Expo's status page does not say anything about
> restarts, so this repo does not claim any.

Expo facts come from Expo's own status page (incident of 26-27 Nov 2019):
https://status.expo.dev/incidents/fq334tqm9grh
Probe behaviour: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/

Tested with kubectl v1.34.2, minikube v1.35.0 (docker driver) and the
`python:3.11-slim` image on Windows 11 (Git Bash), 2026-10-27.
Names are fictional (orders-api, old-db, db-proxy).

## Run it

You need Docker running, minikube and kubectl.

    minikube start --driver=docker
    kubectl create configmap proxy-code --from-file=proxy.py
    kubectl apply -f old-db.yaml
    kubectl apply -f deployment.yaml          # 2 pods, both 2/2
    kubectl delete -f old-db.yaml             # the "unused" database
    kubectl scale deployment orders-api --replicas=4
    kubectl get pods -l app=orders-api        # 2 new pods stay 1/2
    kubectl get endpoints orders-api          # only 2 addresses
    kubectl apply -f deployment-fixed.yaml    # fix 1: no helper, 4 pods 1/1
    kubectl apply -f deployment-liveness.yaml # fix 2: liveness check, RESTARTS climbs

`bash capture.sh` runs the whole sequence and writes `real_run_log.txt`.
Clean up with:

    kubectl delete deployment orders-api old-db
    kubectl delete service orders-api old-db
    kubectl delete configmap proxy-code
    minikube stop

## The three fixes

1. Search before you delete: `grep -n old-db proxy.py deployment.yaml`.
2. Add a liveness check, so a dead helper is restarted loudly, not left silent.
3. See `1/2`? Look at the helper container and its readiness check.

## real_output

`real_output/real_run_log.txt` is the real output from my run.
Pod addresses are local to my minikube cluster.
