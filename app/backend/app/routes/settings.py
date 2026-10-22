"""
Endpoints for Field Representative Preferences, working hours, vehicle type, and routing heuristics.
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from app.auth.jwt_handler import get_current_user

router = APIRouter()

# In-memory preference storage fallback for demo reps
REPRESENTATIVE_PREFERENCES = {
    "full_name": "Parth Lokhande",
    "rep_id": "MR-4092",
    "territory": "Pune Central (Kothrud & Deccan Zone)",
    "vehicle": "two_wheeler",
    "start_location": "home",
    "shift_start": "09:30",
    "shift_end": "18:30",
    "avg_visit_time": 15,
    "lunch_start": "13:30",
    "lunch_end": "14:30",
    "target_visits": 8,
    "opt_strategy": "balanced",
    "auto_carryover": True,
    "traffic_reroute": True,
    "whatsapp_alerts": True,
}


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


@router.get("/profile")
async def get_preferences(user: dict = Depends(get_current_user)):
    """Retrieve current field representative settings."""
    prefs = dict(REPRESENTATIVE_PREFERENCES)
    if user.get("name"):
        prefs["full_name"] = user.get("name")
    if user.get("territory"):
        prefs["territory"] = user.get("territory")
    return {"preferences": prefs}


@router.patch("/profile")
async def update_preferences(payload: SettingsUpdatePayload, user: dict = Depends(get_current_user)):
    """Update representative preferences and routing parameters."""
    data = payload.dict(exclude_unset=True)
    for key, val in data.items():
        if val is not None:
            REPRESENTATIVE_PREFERENCES[key] = val
    return {
        "success": True,
        "detail": "Preferences saved successfully",
        "preferences": REPRESENTATIVE_PREFERENCES,
    }
