# Self-check only (not on screen): biggest retry wave for full jitter over many seeds.
import random, statistics
src = open("main.py").read().split("random.seed(1)")[0]
exec(src)
peaks = []
for seed in range(1, 201):
    random.seed(seed)
    peaks.append(max(retries(jitter).values()))
print("seeds: 200")
print("biggest wave, full jitter: min", min(peaks), "median", statistics.median(peaks), "max", max(peaks))
random.seed(1)
print("fixed wait biggest wave:", max(retries(fixed).values()))
print("backoff biggest wave:", max(retries(backoff).values()))
