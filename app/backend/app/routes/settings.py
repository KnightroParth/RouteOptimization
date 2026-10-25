"""
Endpoints for Field Representative Preferences, working hours, vehicle type, and routing heuristics.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.auth.jwt_handler import require_role
from app.db import get_supabase

router = APIRouter()

# Endpoints for persisted medical representative preferences.

class SettingsUpdatePayload(BaseModel):
    territory: Optional[str] = None
    vehicle: Optional[str] = None
    start_location: Optional[str] = None
    shift_start: Optional[str] = None
    shift_end: Optional[str] = None
    avg_visit_time: Optional[int] = None
    lunch_start: Optional[str] = None
    lunch_end: Optional[str] = None
    target_visits: Optional[int] = None
    opt_strategy: Optional[str] = None
    auto_carryover: Optional[bool] = None
    traffic_reroute: Optional[bool] = None
    whatsapp_alerts: Optional[bool] = None


def _get_profile(user: dict) -> tuple:
    result = (
        get_supabase()
        .table("medical_representatives")
        .select("*")
        .eq("user_id", user["id"])
        .execute()
    )
    if not result.data:
        raise HTTPException(status_code=404, detail="Representative profile not found")
    return result.data[0], user


def _preferences(profile: dict, user: dict) -> dict:
    stored = profile.get("preferences") or {}
    return {
        "full_name": user.get("name", ""),
        "rep_id": profile.get("id"),
        "territory": profile.get("territory", "Pune"),
        "vehicle": profile.get("vehicle_type", "two_wheeler"),
        "start_location": profile.get("start_location", "home"),
        "shift_start": profile.get("working_start", "09:00"),
        "shift_end": profile.get("working_end", "18:00"),
        "avg_visit_time": profile.get("avg_visit_time", 15),
        "lunch_start": profile.get("lunch_start", "13:30"),
        "lunch_end": profile.get("lunch_end", "14:30"),
        "target_visits": profile.get("target_visits_per_day", 8),
        "opt_strategy": profile.get("opt_strategy", "balanced"),
        "auto_carryover": stored.get("auto_carryover", True),
        "traffic_reroute": stored.get("traffic_reroute", True),
        "whatsapp_alerts": stored.get("whatsapp_alerts", True),
    }


@router.get("/profile")
async def get_preferences(user: dict = Depends(require_role("mr"))):
    """Retrieve persisted settings for the authenticated representative."""
    profile, user = _get_profile(user)
    return {"preferences": _preferences(profile, user)}


@router.patch("/profile")
async def update_preferences(
    payload: SettingsUpdatePayload,
    user: dict = Depends(require_role("mr")),
):
    """Persist settings for the authenticated representative only."""
    profile, user = _get_profile(user)
    data = payload.model_dump(exclude_unset=True)
    column_mapping = {
        "vehicle": "vehicle_type",
        "start_location": "start_location",
        "shift_start": "working_start",
        "shift_end": "working_end",
        "lunch_start": "lunch_start",
        "lunch_end": "lunch_end",
        "target_visits": "target_visits_per_day",
        "opt_strategy": "opt_strategy",
        "territory": "territory",
    }
    update_data = {
        column_mapping[key]: value
        for key, value in data.items()
        if key in column_mapping
    }

    preferences = dict(profile.get("preferences") or {})
    for key in ("auto_carryover", "traffic_reroute", "whatsapp_alerts"):
        if key in data:
            preferences[key] = data[key]
    if preferences != (profile.get("preferences") or {}):
        update_data["preferences"] = preferences

    if "avg_visit_time" in data:
        update_data["avg_visit_time"] = data["avg_visit_time"]

    if update_data:
        (
            get_supabase()
            .table("medical_representatives")
            .update(update_data)
            .eq("user_id", user["id"])
            .execute()
        )
        profile.update(update_data)

    return {"success": True, "preferences": _preferences(profile, user)}
