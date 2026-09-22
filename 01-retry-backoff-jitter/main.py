import random

def retries(wait, workers=100, tries=5):
    seconds = {}
    for w in range(workers):
        t = 0
        for n in range(1, tries):
            t += wait(n)
            second = int(t)
            seconds[second] = seconds.get(second, 0) + 1
    return seconds

def show(name, wait):
    calls = retries(wait)
    print(name)
    for s in range(8):
        n = calls.get(s, 0)
        print(f"{s:3d} {'#' * (n // 5):<20} {n}")

def fixed(n):
    return 1

def backoff(n):
    return min(30, 2 ** n)

def jitter(n):
    return random.uniform(0, min(30, 2 ** n))

random.seed(1)

show("fixed wait, 1 second", fixed)
show("backoff", backoff)
show("full jitter", jitter)
