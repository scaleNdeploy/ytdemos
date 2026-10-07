"""Create the demo files ONCE. Harmless by design.
- model.pkl: a normal-looking weights dict, but one item's __reduce__ makes
  loading PRINT a line. That is the whole payload: a print. Nothing else.
  (A real attacker would swap the print for something harmful -- we do not.)
- weights.npz: the same weights, to re-save safely with safetensors.
"""
import pickle
import numpy as np

rng = np.random.default_rng(0)
weights = {"layer1.weight": rng.standard_normal((4, 4)).astype("float32"),
           "layer1.bias": rng.standard_normal(4).astype("float32")}


class RunsOnLoad:
    def __reduce__(self):
        # pickle will CALL this on load. Here it only prints -- harmless.
        msg = "[!] arbitrary code ran when you loaded this file"
        return (print, (msg,))


payload = dict(weights)
payload["_extra"] = RunsOnLoad()           # hidden among normal-looking keys
pickle.dump(payload, open("step1/model.pkl", "wb"))
np.savez("step2/weights.npz", **weights)
print("wrote step1/model.pkl and step2/weights.npz")
