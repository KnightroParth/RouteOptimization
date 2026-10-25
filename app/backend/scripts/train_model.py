"""
Train a Random Forest classifier for MR visit priority prediction.

Reads synthetic training data, trains with cross-validation,
persists the model as a .pkl file and evaluation metrics as JSON.

Usage: python -m scripts.train_model
Output: app/ml/priority_model.pkl, app/ml/model_metrics.json
"""
import json
import os
import sys

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split
from sklearn.preprocessing import LabelEncoder

ML_DIR = os.path.join(os.path.dirname(__file__), "..", "app", "ml")
DATA_PATH = os.path.join(ML_DIR, "training_data.csv")
MODEL_PATH = os.path.join(ML_DIR, "priority_model.pkl")
METRICS_PATH = os.path.join(ML_DIR, "model_metrics.json")

# Feature columns used by the model — must match inference pipeline
FEATURE_COLS = [
    "days_since_last_visit",
    "visit_frequency",
    "follow_up_required",
    "prescription_volume_encoded",
    "engagement_score",
    "specialty_alignment",
]


def main():
    print("=" * 60)
    print("MR Visit Priority — Random Forest Training Pipeline")
    print("=" * 60)

    # 1. Load data
    if not os.path.exists(DATA_PATH):
        print(f"ERROR: Training data not found at {DATA_PATH}")
        print("Run: python -m scripts.generate_training_data")
        sys.exit(1)

    df = pd.read_csv(DATA_PATH)
    print(f"\n[1/5] Loaded {len(df)} records from {DATA_PATH}")
    print(f"  Class distribution:\n{df['priority_class'].value_counts().to_string()}\n")

    # 2. Feature engineering
    rx_map = {"low": 0, "medium": 1, "high": 2}
    df["prescription_volume_encoded"] = df["prescription_volume"].map(rx_map)

    X = df[FEATURE_COLS].values
    y = df["priority_class"].values

    print(f"[2/5] Feature matrix shape: {X.shape}")
    print(f"  Features: {FEATURE_COLS}")

    # 3. Train/test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\n[3/5] Split: {len(X_train)} train / {len(X_test)} test")

    # 4. Train model
    clf = RandomForestClassifier(
        n_estimators=100,
        criterion="gini",
        max_depth=12,
        min_samples_split=5,
        min_samples_leaf=3,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced",
    )

    # Cross-validation on training set
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(clf, X_train, y_train, cv=cv, scoring="accuracy")
    print(f"\n[4/5] 5-Fold CV Accuracy: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    # Fit on full training set
    clf.fit(X_train, y_train)

    # 5. Evaluate on held-out test set
    y_pred = clf.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average="weighted")
    recall = recall_score(y_test, y_pred, average="weighted")
    f1 = f1_score(y_test, y_pred, average="weighted")
    cm = confusion_matrix(y_test, y_pred, labels=clf.classes_).tolist()

    print(f"\n[5/5] Test Set Evaluation:")
    print(f"  Accuracy:  {accuracy:.4f}")
    print(f"  Precision: {precision:.4f}")
    print(f"  Recall:    {recall:.4f}")
    print(f"  F1 Score:  {f1:.4f}")
    print(f"\n  Confusion Matrix (rows=true, cols=pred):")
    print(f"  Classes: {list(clf.classes_)}")
    for row in cm:
        print(f"    {row}")

    print(f"\n  Classification Report:")
    print(classification_report(y_test, y_pred))

    # Feature importances
    importances = dict(zip(FEATURE_COLS, clf.feature_importances_.tolist()))
    sorted_imp = sorted(importances.items(), key=lambda x: x[1], reverse=True)
    print("  Feature Importances:")
    for name, imp in sorted_imp:
        bar = "#" * int(imp * 50)
        print(f"    {name:35s} {imp:.4f}  {bar}")

    # Save model
    os.makedirs(ML_DIR, exist_ok=True)
    joblib.dump(clf, MODEL_PATH)
    print(f"\n  Model saved to: {MODEL_PATH}")

    # Save metrics
    metrics = {
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1_score": round(f1, 4),
        "cv_accuracy_mean": round(cv_scores.mean(), 4),
        "cv_accuracy_std": round(cv_scores.std(), 4),
        "n_estimators": 100,
        "criterion": "gini",
        "max_depth": 12,
        "n_train": len(X_train),
        "n_test": len(X_test),
        "classes": list(clf.classes_),
        "confusion_matrix": cm,
        "feature_importances": importances,
        "feature_names": FEATURE_COLS,
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=2)
    print(f"  Metrics saved to: {METRICS_PATH}")

    print("\n" + "=" * 60)
    print("Training complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
