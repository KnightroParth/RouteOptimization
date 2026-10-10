"""
ML Priority Engine — Random Forest-based visit priority prediction.

This module provides both a trained model inference path and a rule-based
fallback when no trained model is available.
"""
import os
import numpy as np
from typing import List

# Try to load a trained model; fall back to rule-based
_model = None
_model_version = "rule-based-v1"

try:
    import joblib

    model_path = os.path.join(os.path.dirname(__file__), "..", "ml", "priority_model.pkl")
    if os.path.exists(model_path):
        _model = joblib.load(model_path)
        _model_version = "rf-v1"
except Exception:
    pass


def _rule_based_priority(visit: dict) -> dict:
    """
    Rule-based fallback priority when no trained model is available.
    Uses: follow_up_required, days_since_last_visit, doctor priority_category.
    """
    score = 0.5  # base

    # Follow-up required → boost priority
    if visit.get("follow_up_required"):
        score += 0.25

    # Days since last visit (more days = higher urgency)
    days_since = visit.get("days_since_last_visit", 30)
    if days_since > 60:
        score += 0.2
    elif days_since > 30:
        score += 0.1

    # Doctor's inherent priority category
    cat = (visit.get("priority_category") or "").lower()
    if cat == "high":
        score += 0.15
    elif cat == "medium":
        score += 0.05

    # Specialization boost (certain specialties visited more)
    spec = (visit.get("doctor_specialization") or "").lower()
    high_value_specs = ["cardiologist", "oncologist", "neurologist", "orthopedic"]
    if spec in high_value_specs:
        score += 0.1

    # Clamp 0–1
    score = max(0.0, min(1.0, score))

    # Classify
    if score >= 0.7:
        priority_class = "high"
    elif score >= 0.4:
        priority_class = "medium"
    else:
        priority_class = "low"

    return {
        "priority_class": priority_class,
        "priority_score": round(score, 3),
        "model_version": _model_version,
    }


def _ml_priority(features: np.ndarray) -> dict:
    """Use the trained Random Forest model for prediction."""
    proba = _model.predict_proba(features.reshape(1, -1))[0]
    classes = _model.classes_
    pred_idx = np.argmax(proba)

    return {
        "priority_class": str(classes[pred_idx]),
        "priority_score": round(float(proba[pred_idx]), 3),
        "model_version": _model_version,
    }


def predict_priority(visit: dict) -> dict:
    """
    Predict visit priority using either the trained model or rule-based fallback.

    Args:
        visit: dict with keys like follow_up_required, days_since_last_visit,
               priority_category, doctor_specialization, visit_frequency, etc.

    Returns:
        dict with priority_class, priority_score, model_version
    """
    if _model is not None:
        try:
            # Extract features in the expected order
            features = np.array([
                visit.get("days_since_last_visit", 30),
                visit.get("visit_frequency", 1),
                1 if visit.get("follow_up_required") else 0,
                visit.get("prescription_volume", 50),
                visit.get("engagement_score", 0.5),
            ])
            return _ml_priority(features)
        except Exception:
            pass

    return _rule_based_priority(visit)


def predict_batch(visits: List[dict]) -> List[dict]:
    """Predict priority for a batch of visits."""
    results = []
    for v in visits:
        pred = predict_priority(v)
        pred["visit_id"] = v.get("visit_id") or v.get("id")
        pred["doctor_id"] = v.get("doctor_id")
        results.append(pred)
    return results
