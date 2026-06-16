"""
Mobile Price Range Prediction - Model Training Pipeline
=========================================================

Loads the dataset, preprocesses it, trains several classification models,
evaluates and compares them, then persists the best-performing model
(plus the fitted scaler and metadata) so the FastAPI backend can serve
predictions.

Run:
    python train_model.py

Outputs (written to this directory):
    model.pkl            -> best trained model (joblib)
    scaler.pkl           -> fitted StandardScaler (joblib)
    feature_names.json   -> ordered list of feature columns expected by the model
    metrics.json         -> evaluation metrics for every model trained
    confusion_matrix.png -> confusion matrix of the best model
    feature_importance.png -> feature importance chart (if supported by best model)
"""

import json
import warnings
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT.parent / "data" / "train.csv"
RANDOM_STATE = 42


def load_data():
    df = pd.read_csv(DATA_PATH)
    X = df.drop(columns=["price_range"])
    y = df["price_range"]
    return X, y


def build_models():
    models = {
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
        "KNN": KNeighborsClassifier(n_neighbors=9),
        "Decision Tree": DecisionTreeClassifier(max_depth=8, random_state=RANDOM_STATE),
        "Random Forest": RandomForestClassifier(
            n_estimators=200, max_depth=12, random_state=RANDOM_STATE
        ),
        "SVM (RBF)": SVC(kernel="rbf", C=10, gamma="scale", probability=True, random_state=RANDOM_STATE),
        "Gradient Boosting": GradientBoostingClassifier(
            n_estimators=150, max_depth=3, learning_rate=0.1, random_state=RANDOM_STATE
        ),
    }

    # XGBoost is optional - include it automatically if it's installed
    try:
        from xgboost import XGBClassifier

        models["XGBoost"] = XGBClassifier(
            n_estimators=200,
            max_depth=5,
            learning_rate=0.1,
            random_state=RANDOM_STATE,
            eval_metric="mlogloss",
            verbosity=0,
        )
    except ImportError:
        print("xgboost not installed - skipping (pip install xgboost to include it)")

    return models


def main():
    X, y = load_data()
    feature_names = list(X.columns)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    models = build_models()
    results = {}
    fitted_models = {}

    print(f"{'Model':<20} {'Accuracy':>9} {'Precision':>10} {'Recall':>8} {'F1':>8} {'CV Acc':>8}")
    print("-" * 70)

    for name, model in models.items():
        model.fit(X_train_scaled, y_train)
        preds = model.predict(X_test_scaled)

        acc = accuracy_score(y_test, preds)
        prec = precision_score(y_test, preds, average="macro")
        rec = recall_score(y_test, preds, average="macro")
        f1 = f1_score(y_test, preds, average="macro")
        cv_acc = cross_val_score(model, X_train_scaled, y_train, cv=5).mean()

        results[name] = {
            "accuracy": round(acc, 4),
            "precision_macro": round(prec, 4),
            "recall_macro": round(rec, 4),
            "f1_macro": round(f1, 4),
            "cv_accuracy_mean": round(cv_acc, 4),
        }
        fitted_models[name] = model

        print(f"{name:<20} {acc:>9.4f} {prec:>10.4f} {rec:>8.4f} {f1:>8.4f} {cv_acc:>8.4f}")

    # Pick best model by cross-validated accuracy (more robust than a single split)
    best_name = max(results, key=lambda n: results[n]["cv_accuracy_mean"])
    best_model = fitted_models[best_name]
    print(f"\nBest model: {best_name}")
    print(json.dumps(results[best_name], indent=2))

    # ---- Persist artifacts ----
    joblib.dump(best_model, ROOT / "model.pkl")
    joblib.dump(scaler, ROOT / "scaler.pkl")

    with open(ROOT / "feature_names.json", "w") as f:
        json.dump(feature_names, f, indent=2)

    metrics_out = {
        "best_model": best_name,
        "results": results,
        "class_labels": {
            "0": "Low Cost",
            "1": "Medium Cost",
            "2": "High Cost",
            "3": "Very High Cost",
        },
    }
    with open(ROOT / "metrics.json", "w") as f:
        json.dump(metrics_out, f, indent=2)

    # ---- Confusion matrix plot ----
    best_preds = best_model.predict(X_test_scaled)
    cm = confusion_matrix(y_test, best_preds)
    fig, ax = plt.subplots(figsize=(5, 4))
    ConfusionMatrixDisplay(cm, display_labels=["0 Low", "1 Medium", "2 High", "3 Very High"]).plot(
        ax=ax, cmap="Blues", colorbar=False
    )
    ax.set_title(f"Confusion Matrix - {best_name}")
    plt.tight_layout()
    plt.savefig(ROOT / "confusion_matrix.png", dpi=150)
    plt.close(fig)

    # ---- Feature importance plot (if supported) ----
    importances = None
    if hasattr(best_model, "feature_importances_"):
        importances = best_model.feature_importances_
    elif hasattr(best_model, "coef_"):
        importances = np.abs(best_model.coef_).mean(axis=0)

    if importances is not None:
        order = np.argsort(importances)[::-1]
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.barplot(
            x=importances[order],
            y=np.array(feature_names)[order],
            ax=ax,
            color="#3b82f6",
        )
        ax.set_title(f"Feature Importance - {best_name}")
        ax.set_xlabel("Importance")
        plt.tight_layout()
        plt.savefig(ROOT / "feature_importance.png", dpi=150)
        plt.close(fig)

    print("\nSaved model.pkl, scaler.pkl, feature_names.json, metrics.json")


if __name__ == "__main__":
    main()
