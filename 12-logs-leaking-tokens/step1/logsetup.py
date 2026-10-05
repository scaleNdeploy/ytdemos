import logging
import sys

def setup():
    h = logging.StreamHandler(sys.stderr)
    fmt = logging.Formatter("%(levelname)s %(message)s")
    h.setFormatter(fmt)
    logging.basicConfig(level=logging.DEBUG,
                        handlers=[h], force=True)
