# Loading a model file can run code

Video: (link added after upload)
Short: (link added after upload)

> **Safety note.** This repo demonstrates, defensively, that loading an
> untrusted pickle-based model file can run code. The demo payload here is
> **harmless: it only prints a line.** There are no shell commands, no file
> writes, no network calls anywhere. A real attacker would swap that print
> for something harmful; this repo does not show how. The point is the fix.

Needs Python 3.10+ (tested 3.10.12), numpy, and safetensors.

    pip install -r requirements.txt

Everything is fictional: the company (parcelpath) and the weights. The
tokens/keys idea from other videos does not appear here.

## First make the demo files (once)

    python make_files.py

This writes `step1/model.pkl` (a normal-looking weights dict whose one extra
item prints a line when unpickled) and `step2/weights.npz` (the same weights,
to re-save safely).

## step1 - loading it runs code

    cd step1
    python load_model.py

You never called the model. Opening the file printed a line, which means it
ran code. A machine learning model saved with pickle (`.pkl`) can do this.

## step2 - the fix: safetensors

    cd step2
    python save_safe.py     # weights -> model.safetensors
    python load_safe.py     # same weights back

safetensors stores only tensors and names. There is no place for code, so
loading a safetensors file cannot run anything.

## step3 - check before you load

    cd step3
    cp ../step1/model.pkl .
    cp ../step2/model.safetensors .
    python scan.py model.pkl model.safetensors

`scan.py` reads a file with `pickletools` (it never loads it) and flags one
that contains code-execution opcodes. The pickle is FLAGged; the safetensors
file is OK.

## It's not just .pkl

PyTorch's own saved weights -- `.pt`, `.bin`, `.ckpt` -- are pickle
underneath. Hugging Face: "PyTorch model weights are commonly saved and
stored as `.bin` files with Python's pickle utility." Same risk, different
name. safetensors is the one format that is just data.

## If you already loaded a bad one

You can't un-run code. Treat that machine as compromised: rotate anything it
could reach, and rebuild it.

## Sources

- JFrog, 27 Feb 2024: ~100 malicious models found on Hugging Face that ran
  code when loaded (pickle-based):
  https://jfrog.com/blog/data-scientists-targeted-by-malicious-hugging-face-ml-models-with-silent-backdoor/
- Hugging Face safetensors: https://huggingface.co/docs/safetensors/index
- Python docs (pickle): "The pickle module is not secure. Only unpickle data
  you trust." https://docs.python.org/3/library/pickle.html
