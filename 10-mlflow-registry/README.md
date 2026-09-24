# Which model is in production? Experiment tracking with MLflow

Video: (link added after upload)
Short: (link added after upload)

Needs Python 3.10 or newer, `scikit-learn`, `joblib`, and
[`mlflow`](https://mlflow.org/) (3.16.1 or newer, tested against that
version).

    pip install scikit-learn joblib mlflow

Everything here is fictional: the company ("Northlane Payments") and
its fraud-scoring model. The data is synthetic (`sklearn.datasets.make_classification`
with a fixed seed), and the MLflow behaviour shown (the retired
file-store backend, and `search_model_versions().aliases` coming back
empty) is real, reproduced against a real local MLflow server, not
invented.

## Run it

    python main.py

This runs the story's fixed ending in one shot:
1. Trains two model versions ("v1" on a small subset, "v2" on the
   full training set) and logs each as an MLflow run: params, the
   accuracy metric, and the model itself, registered as `fraud_model`.
2. Marks version 2 with the `production` alias.
3. Shows the wrong way to check which version is live
   (`client.search_model_versions()` — its `.aliases` field comes back
   empty even after the alias is set, at least on MLflow 3.16.1).
4. Shows the reliable way: `client.get_model_version_by_alias(name,
   "production")`.

By default this uses a local SQLite backend (`sqlite:///mlflow.db`,
created next to this script, reset on every run for repeatable
output). To browse it in the UI:

    mlflow ui --backend-store-uri sqlite:///mlflow.db

## The mistake, for comparison

`train_v1_and_v2_old_way()` is the "before" version from the video:
it trains the same two models but saves each with plain
`joblib.dump(model, "fraud_model.pkl")`, so the second run silently
overwrites the first with no history. It's in this file but not
called by default; see the video for the full before/after story.

## A real gotcha along the way

Older MLflow tutorials show `mlflow.set_tracking_uri("file:./mlruns")`.
On current MLflow (3.x) this raises an error telling you the
filesystem tracking backend is in maintenance mode and to use a
database backend instead — which is why this script uses
`sqlite:///mlflow.db`. Confirmed by actually hitting the error.

## Limits

Tested against MLflow 3.16.1 on 2026-09-24. The `search_model_versions()`
aliases-empty behaviour is a real quirk of that version; a future
MLflow release may fix it (there's an open-ish GitHub issue trail for
similar alias bugs). If you see aliases populated there on a newer
version, that's a good sign, not a bug in this code.
