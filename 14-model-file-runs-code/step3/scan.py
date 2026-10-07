"""Can this file run code when loaded? Read-only:
we list the opcodes, we never load the file."""
import pickletools
import sys

# opcodes that call a function / build an object
RISKY = {"REDUCE", "GLOBAL", "STACK_GLOBAL"}


def scan(path):
    if path.endswith(".safetensors"):
        print(f"OK    {path}: tensors only")
        return
    with open(path, "rb") as f:
        ops = {op.name for op, _, _ in pickletools.genops(f)}
    bad = ops & RISKY
    if bad:
        print(f"FLAG  {path}: can run code")
    else:
        print(f"OK    {path}: no code")


for p in sys.argv[1:]:
    scan(p)
