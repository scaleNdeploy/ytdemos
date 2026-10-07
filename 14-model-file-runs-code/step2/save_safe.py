import numpy as np
from safetensors.numpy import save_file

data = np.load("weights.npz")
weights = {k: data[k] for k in data.files}
save_file(weights, "model.safetensors")
print("saved model.safetensors")
