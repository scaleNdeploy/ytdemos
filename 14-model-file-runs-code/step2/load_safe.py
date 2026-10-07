from safetensors.numpy import load_file

weights = load_file("model.safetensors")
for name, w in weights.items():
    print(name, w.shape)
