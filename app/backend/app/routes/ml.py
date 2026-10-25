"""
Endpoints for Random Forest ML model analysis, feature importance weights, and batch inference.
"""
import json
import os
from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timezone
from time import perf_counter
from app.auth.jwt_handler import get_current_user
from app.db import get_supabase
from app.services.priority import predict_batch

router = APIRouter()

# Load trained model metrics if available
_metrics_path = os.path.join(os.path.dirname(__file__), "..", "ml", "model_metrics.json")
_model_metrics = None
try:
    if os.path.exists(_metrics_path):
        with open(_metrics_path) as f:
            _model_metrics = json.load(f)
except Exception:
    pass

# Human-readable feature descriptions
_FEATURE_DESCRIPTIONS = {
    "days_since_last_visit": "Doctors overdue for detailing receive highest urgency boost",
    "prescription_volume_encoded": "Tier-1 hospital prescribers weighted for maximum business conversion",
    "engagement_score": "Responsiveness ratio of doctor to past medical representative detailing",
    "follow_up_required": "Pending follow-up visits flagged for immediate scheduling",
    "visit_frequency": "Low visit frequency increases scheduling priority",
    "specialty_alignment": "Strategic match with active pharmaceutical campaign drugs",
}

_FEATURE_DISPLAY_NAMES = {
    "days_since_last_visit": "Days Since Last Visit (Recency)",
    "prescription_volume_encoded": "Prescription Volume (Rx Potential)",
    "engagement_score": "Historical Conversion Rate",
    "follow_up_required": "Follow-Up Required",
    "visit_frequency": "Visit Frequency",
    "specialty_alignment": "Specialty Category Alignment",
}


def _build_feature_weights():
    """Build feature weights from trained model metrics or use defaults."""
    if _model_metrics and "feature_importances" in _model_metrics:
        importances = _model_metrics["feature_importances"]
        weights = []
        for feat_name, imp in sorted(importances.items(), key=lambda x: x[1], reverse=True):
            weights.append({
                "name": _FEATURE_DISPLAY_NAMES.get(feat_name, feat_name),
                "weight": round(imp, 4),
                "percentage": round(imp * 100, 1),
                "description": _FEATURE_DESCRIPTIONS.get(feat_name, ""),
            })
        return weights

    # Fallback hardcoded weights
    return [
        {"name": "Days Since Last Visit (Recency)", "weight": 0.40, "percentage": 40,
         "description": "Doctors overdue for detailing receive highest urgency boost"},
        {"name": "Prescription Volume (Rx Potential)", "weight": 0.18, "percentage": 18,
         "description": "Tier-1 hospital prescribers weighted for maximum business conversion"},
        {"name": "Historical Conversion Rate", "weight": 0.15, "percentage": 15,
         "description": "Responsiveness ratio of doctor to past medical representative detailing"},
        {"name": "Follow-Up Required", "weight": 0.11, "percentage": 11,
         "description": "Pending follow-up visits flagged for immediate scheduling"},
        {"name": "Visit Frequency", "weight": 0.09, "percentage": 9,
         "description": "Low visit frequency increases scheduling priority"},
        {"name": "Specialty Category Alignment", "weight": 0.07, "percentage": 7,
         "description": "Strategic match with active pharmaceutical campaign drugs"},
    ]


@router.get("/feature-importance")
async def get_feature_importance(user: dict = Depends(get_current_user)):
    """Return Random Forest feature importance weights from trained model."""
    metrics = _model_metrics or {}
    return {
        "model": "RandomForestClassifier",
        "n_estimators": metrics.get("n_estimators", 100),
        "criterion": metrics.get("criterion", "gini"),
        "max_depth": metrics.get("max_depth", 12),
        "feature_weights": _build_feature_weights(),
        "accuracy": metrics.get("accuracy"),
        "precision": metrics.get("precision"),
        "recall": metrics.get("recall"),
        "f1_score": metrics.get("f1_score"),
        "cv_accuracy": metrics.get("cv_accuracy_mean"),
        "n_training_samples": metrics.get("n_train"),
        "model_version": "rf-v1" if _model_metrics else "rule-based-v1",
    }


@router.post("/run-batch")
async def run_batch_inference(user: dict = Depends(get_current_user)):
    """Trigger Random Forest batch inference on all clinic profiles."""
    started = perf_counter()
    timestamp = datetime.now(timezone.utc).strftime("%H:%M:%S")
    sb = get_supabase()
    visits_result = (
        sb.table("visits")
        .select("id, doctor_id, mr_id, follow_up_required, doctors(specialization, priority_category)")
        .execute()
    )
    visits = visits_result.data or []

    # Compute visit recency and frequency per doctor from completed visits
    recency_map = {}  # doctor_id -> days since last completed visit
    frequency_map = {}  # doctor_id -> count of completed visits
    try:
        history = (
            sb.table("visits")
            .select("doctor_id, visit_date")
            .eq("status", "completed")
            .order("visit_date", desc=True)
            .execute()
        )
        for row in history.data or []:
            did = row["doctor_id"]
            frequency_map[did] = frequency_map.get(did, 0) + 1
            if did not in recency_map:
                try:
                    from datetime import date as dt_date
                    last_date = dt_date.fromisoformat(row["visit_date"])
                    recency_map[did] = (dt_date.today() - last_date).days
                except (ValueError, TypeError):
                    pass
    except Exception:
        pass

    prediction_inputs = []
    for visit in visits:
        doctor = visit.get("doctors") or {}
        did = visit.get("doctor_id")
        prediction_inputs.append({
            "id": visit["id"],
            "visit_id": visit["id"],
            "doctor_id": did,
            "doctor_specialization": doctor.get("specialization"),
            "priority_category": doctor.get("priority_category"),
            "follow_up_required": visit.get("follow_up_required", False),
            "days_since_last_visit": recency_map.get(did, 90),
            "visit_frequency": frequency_map.get(did, 0),
        })

    predictions = predict_batch(prediction_inputs)
    counts = {"high": 0, "medium": 0, "low": 0, "total": len(predictions)}
    for visit, prediction in zip(prediction_inputs, predictions):
        priority_class = prediction["priority_class"]
        if priority_class in counts:
            counts[priority_class] += 1
        sb.table("priority_predictions").insert({
            "visit_id": visit["visit_id"],
            "priority_class": priority_class,
            "priority_score": prediction["priority_score"],
            "model_version": prediction["model_version"],
        }).execute()

    duration_ms = round((perf_counter() - started) * 1000, 2)
    logs = [
        f"[{timestamp}] Starting priority inference pipeline...",
        f"[{timestamp}] Loaded {len(visits)} visits from database.",
        f"[{timestamp}] Generated {len(predictions)} priority predictions.",
        f"[{timestamp}] Counts: {counts['high']} high, {counts['medium']} medium, {counts['low']} low.",
        f"[{timestamp}] Batch completed in {duration_ms}ms.",
    ]

    return {
        "success": True,
        "timestamp": timestamp,
        "duration_ms": duration_ms,
        "counts": counts,
        "logs": logs,
    }


@router.get("/results")
async def get_priority_results(
    mr_id: str | None = Query(None),
    date: str | None = Query(None),
    user: dict = Depends(get_current_user),
):
    """Return the latest persisted priority prediction for each requested visit."""
    if user.get("role") == "mr":
        if mr_id and mr_id != user.get("mr_id"):
            raise HTTPException(status_code=403, detail="Not authorized for this representative")
        mr_id = user.get("mr_id")

    visits_query = get_supabase().table("visits").select(
        "id, doctor_id, visit_date, doctors(name, specialization)"
    )
    if mr_id:
        visits_query = visits_query.eq("mr_id", mr_id)
    if date:
        visits_query = visits_query.eq("visit_date", date)
    visits = visits_query.execute().data or []
    visit_ids = [visit["id"] for visit in visits]
    if not visit_ids:
        return {"results": []}

    predictions = get_supabase().table("priority_predictions").select(
        "visit_id, priority_class, priority_score, predicted_at"
    ).in_("visit_id", visit_ids).order("predicted_at", desc=True).execute().data or []
    latest = {}
    for prediction in predictions:
        latest.setdefault(prediction["visit_id"], prediction)

    results = []
    for visit in visits:
        prediction = latest.get(visit["id"])
        if not prediction:
            continue
        doctor = visit.get("doctors") or {}
        results.append({
            "id": visit["id"],
            "name": doctor.get("name", "Unknown Doctor"),
            "specialty": doctor.get("specialization", "General"),
            "score": prediction["priority_score"],
            "priority": prediction["priority_class"],
            "confidence": None,
            "visit_date": visit.get("visit_date"),
        })

    return {"results": sorted(results, key=lambda item: item["score"], reverse=True)}
