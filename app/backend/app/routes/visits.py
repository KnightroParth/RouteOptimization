"""Visit management endpoints."""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from app.models.schemas import VisitCreate, VisitResponse, VisitStatusUpdate, VisitUpdate
from app.auth.jwt_handler import get_current_user
from app.db import get_supabase

router = APIRouter()


@router.get("/")
async def list_visits(
    mr_id: Optional[str] = Query(None),
    date: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    user: dict = Depends(get_current_user),
):
    """List visits with optional filters."""
    sb = get_supabase()
    query = sb.table("visits").select("*, doctors(name, specialization, latitude, longitude)")

    if mr_id:
        query = query.eq("mr_id", mr_id)
    if date:
        query = query.eq("visit_date", date)
    if status:
        query = query.eq("status", status)

    result = query.order("visit_date", desc=True).execute()

    # Flatten the joined doctor data
    visits = []
    for v in result.data or []:
        doctor = v.pop("doctors", None) or {}
        v["doctor_name"] = doctor.get("name")
        v["doctor_specialization"] = doctor.get("specialization")
        v["doctor_latitude"] = doctor.get("latitude")
        v["doctor_longitude"] = doctor.get("longitude")
        visits.append(v)

    return {"visits": visits}


@router.get("/daily")
async def get_daily_visits(
    mr_id: str = Query(...),
    date: str = Query(...),
    user: dict = Depends(get_current_user),
):
    """Get all visits for an MR on a specific date with priority predictions."""
    sb = get_supabase()

    # Fetch visits with doctor and priority data
    result = (
        sb.table("visits")
        .select("*, doctors(name, specialization, latitude, longitude, availability_start, availability_end, typical_visit_duration)")
        .eq("mr_id", mr_id)
        .eq("visit_date", date)
        .execute()
    )

    visits = []
    for v in result.data or []:
        doctor = v.pop("doctors", None) or {}
        v["doctor_name"] = doctor.get("name")
        v["doctor_specialization"] = doctor.get("specialization")
        v["doctor_latitude"] = doctor.get("latitude")
        v["doctor_longitude"] = doctor.get("longitude")
        v["availability_start"] = doctor.get("availability_start")
        v["availability_end"] = doctor.get("availability_end")
        v["typical_visit_duration"] = doctor.get("typical_visit_duration", 30)

        # Fetch priority prediction if exists
        pred = (
            sb.table("priority_predictions")
            .select("priority_class, priority_score")
            .eq("visit_id", v["id"])
            .order("predicted_at", desc=True)
            .limit(1)
            .execute()
        )
        if pred.data:
            v["priority_class"] = pred.data[0]["priority_class"]
            v["priority_score"] = pred.data[0]["priority_score"]
        else:
            v["priority_class"] = None
            v["priority_score"] = None

        visits.append(v)

    return {"visits": visits, "date": date, "mr_id": mr_id}


@router.post("/", status_code=201)
async def create_visit(visit: VisitCreate, user: dict = Depends(get_current_user)):
    """Create a new visit."""
    sb = get_supabase()
    result = sb.table("visits").insert(visit.model_dump()).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create visit")
    return result.data[0]


@router.patch("/{visit_id}/status")
async def update_visit_status(
    visit_id: str,
    update: VisitStatusUpdate,
    user: dict = Depends(get_current_user),
):
    """Update a visit's status and optional outcome."""
    sb = get_supabase()
    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    update_data["status"] = update.status.value

    result = (
        sb.table("visits")
        .update(update_data)
        .eq("id", visit_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Visit not found")
    return result.data[0]


@router.put("/{visit_id}")
async def update_visit(
    visit_id: str,
    update: VisitUpdate,
    user: dict = Depends(get_current_user),
):
    """Full update of a visit record."""
    sb = get_supabase()
    update_data = {k: v for k, v in update.model_dump().items() if v is not None}
    if "status" in update_data and hasattr(update_data["status"], "value"):
        update_data["status"] = update_data["status"].value

    result = (
        sb.table("visits")
        .update(update_data)
        .eq("id", visit_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Visit not found")
    return result.data[0]


@router.delete("/{visit_id}", status_code=204)
async def delete_visit(
    visit_id: str,
    user: dict = Depends(get_current_user),
):
    """Delete a visit record."""
    sb = get_supabase()
    sb.table("visits").delete().eq("id", visit_id).execute()
    return None

