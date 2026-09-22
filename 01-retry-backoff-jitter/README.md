# Retry storms: backoff and jitter

Video: https://youtu.be/iQDTcKd88KU
Short: https://www.youtube.com/shorts/Z5dOI18ZC2M

Needs Python 3.10 or newer. No other packages.

## Run it

One worker with a retry loop (`api.py` fails twice, then works):

    python one.py

Count when 100 workers retry, with three wait rules:

    python main.py

Check the jitter result over 200 random seeds (not shown in the video):

    python check_seeds.py

## Limits

The count is a simple model. It assumes the service stays down, so every
retry fails. It shows when retries land, not whether a service recovers.
