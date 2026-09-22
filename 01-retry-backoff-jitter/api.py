failures = {"left": 2}

def call_api():
    if failures["left"] > 0:
        failures["left"] -= 1
        raise ConnectionError("payments-api is down")
    return "ok"
