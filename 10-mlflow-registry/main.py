import os
os.environ.setdefault("MLFLOW_DISABLE_TELEMETRY", "true")
import mlflow
from mlflow import MlflowClient
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import joblib


def make_transactions():
    X, y = make_classification(
        n_samples=600, n_features=6, n_informative=4,
        n_redundant=0, class_sep=0.7, random_state=4)
    return train_test_split(
        X, y, test_size=120, random_state=4)


def train_old_way(X, y, out_path):
    model = LogisticRegression().fit(X, y)
    joblib.dump(model, out_path)
    return model


def train_v1_and_v2_old_way():
    X_tr, X_te, y_tr, y_te = make_transactions()
    m1 = train_old_way(X_tr[:60], y_tr[:60],
                        "fraud_model.pkl")
    print(f"v1 saved. test score: "
          f"{m1.score(X_te, y_te):.2f}")
    m2 = train_old_way(X_tr, y_tr, "fraud_model.pkl")
    print(f"v2 saved. test score: "
          f"{m2.score(X_te, y_te):.2f}")
    print("disk still shows one file: fraud_model.pkl")


def train_and_log(name, X, y, X_te, y_te, run_name):
    with mlflow.start_run(run_name=run_name):
        model = LogisticRegression().fit(X, y)
        acc = model.score(X_te, y_te)
        mlflow.log_param("rows", len(X))
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(
            model, name="model",
            registered_model_name=name)
        return acc


def mark_production(name, version):
    client = MlflowClient()
    client.set_registered_model_alias(
        name, "production", version)


def which_is_live_wrong(name):
    client = MlflowClient()
    versions = client.search_model_versions(
        f"name='{name}'")
    for v in versions:
        print(f"version {v.version}: "
              f"aliases={v.aliases}")


def which_is_live_fixed(name):
    client = MlflowClient()
    mv = client.get_model_version_by_alias(
        name, "production")
    print(f"production is version {mv.version}")


def main():
    if os.path.exists("mlflow.db"):
        os.remove("mlflow.db")
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("fraud-scoring")
    X_tr, X_te, y_tr, y_te = make_transactions()

    v1_acc = train_and_log(
        "fraud_model", X_tr[:60], y_tr[:60],
        X_te, y_te, "v1")
    v2_acc = train_and_log(
        "fraud_model", X_tr, y_tr, X_te, y_te, "v2")
    print(f"v1 test accuracy: {v1_acc:.2f}")
    print(f"v2 test accuracy: {v2_acc:.2f}")

    mark_production("fraud_model", 2)

    print("-- search_model_versions --")
    which_is_live_wrong("fraud_model")
    print("-- get_model_version_by_alias --")
    which_is_live_fixed("fraud_model")


if __name__ == "__main__":
    main()
