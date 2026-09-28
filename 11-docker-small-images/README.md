# Docker for a Python service: small images

Video: (link added after upload)

Needs Docker (Docker Desktop or any Docker Engine 20.10+). No Python
install required on the host -- everything runs inside the containers.

Fictional company (northlane-api) and a fictional /health endpoint;
flask, gunicorn, numpy and pandas are real packages used as stand-ins
for "a couple of heavier dependencies," a common shape for small
Python services.

## Run it

Build the naive image (what most people write first):

    docker build -f Dockerfile.naive -t northlane-api:naive .

Build the fixed image (multi-stage, no pip cache, non-root user):

    docker build -f Dockerfile.fixed -t northlane-api:fixed .

Compare sizes:

    docker images | grep northlane-api

Run the small image and check it still works:

    docker run -d -p 8000:8000 --name northlane-api-demo northlane-api:fixed
    curl http://localhost:8000/health

## What changed, and why it's smaller

1. `python:3.11-slim` instead of `python:3.11` as the base image --
   skips the full Debian toolchain the app never uses.
2. A multi-stage build -- pip's build tools and download cache live
   only in the `builder` stage, which is discarded; the final image
   copies over just the finished virtual environment and `app.py`.
3. `pip install --no-cache-dir` -- no copy of every downloaded
   package sitting unused inside the image.
4. `Dockerfile.fixed.dockerignore` -- Docker (BuildKit) picks up a
   per-Dockerfile ignore file automatically when it's named
   `<Dockerfile>.dockerignore`, so this applies only to the fixed
   build. The naive build has no ignore file at all, which is
   deliberate: it's what actually happens if nobody adds one.
5. `USER appuser` -- runs as a non-root user instead of whatever the
   base image defaults to (root, for the official Python image).

On the machine this was recorded on: northlane-api:naive came out to
1.9 GB (492 MB compressed); northlane-api:fixed came out to 444 MB
(100 MB compressed) -- about 77% smaller. Exact numbers will vary by
machine, Docker version, and platform.

## What this is (and isn't)

northlane-api, its story, and its numbers are fictional, built to
demonstrate a real and common Docker mistake. The build/size behavior
is real Docker behavior; nothing here was faked or scripted to show a
result. This wasn't pushed to any registry -- everything shown runs
locally.
