import time
from api import call_api

def get_status():
    for attempt in range(1, 6):
        try:
            return call_api()
        except ConnectionError:
            print(f"try {attempt} failed")
            time.sleep(1)
    raise ConnectionError("gave up")

print(get_status())
