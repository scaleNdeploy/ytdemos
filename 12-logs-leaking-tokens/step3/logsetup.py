import logging
import re
import sys

SECRET = re.compile(r"(Bearer |token=|password=)[^\s'\"&]+")

class Scrub(logging.Formatter):
    def format(self, record):
        text = super().format(record)
        return SECRET.sub(r"\1****", text)

def setup():
    h = logging.StreamHandler(sys.stderr)
    h.setFormatter(Scrub("%(levelname)s %(message)s"))
    logging.basicConfig(level=logging.DEBUG,
                        handlers=[h], force=True)
