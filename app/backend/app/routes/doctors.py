"""Doctor management endpoints."""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from app.models.schemas import DoctorCreate, DoctorResponse, DoctorUpdate
from app.auth.jwt_handler import get_current_user
from app.db import get_supabase

router = APIRouter()


@router.get("/")
async def list_doctors(
    territory: Optional[str] = Query(None),
    specialization: Optional[str] = Query(None),
    user: dict = Depends(get_current_user),
):
    """List doctors, optionally filtered by territory or specialization."""
    sb = get_supabase()
    query = sb.table("doctors").select("*")

    if territory:
        query = query.eq("territory", territory)
    if specialization:
        query = query.eq("specialization", specialization)

    result = query.order("name").execute()
    return {"doctors": result.data or []}


@router.get("/{doctor_id}")
async def get_doctor(doctor_id: str, user: dict = Depends(get_current_user)):
    """Get a single doctor by ID."""
    sb = get_supabase()
    result = sb.table("doctors").select("*").eq("id", doctor_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return result.data[0]


@router.post("/", status_code=201)
async def create_doctor(doctor: DoctorCreate, user: dict = Depends(get_current_user)):
    """Create a new doctor record."""
    sb = get_supabase()
    result = sb.table("doctors").insert(doctor.model_dump()).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create doctor")
    return result.data[0]


@router.put("/{doctor_id}")
async def update_doctor(
    doctor_id: str, doctor: DoctorUpdate, user: dict = Depends(get_current_user)
):
    """Update an existing doctor record."""
    sb = get_supabase()
    update_data = {k: v for k, v in doctor.model_dump().items() if v is not None}
    result = (
        sb.table("doctors")
        .update(update_data)
        .eq("id", doctor_id)
        .execute()
    )

    if not result.data:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return result.data[0]


@router.delete("/{doctor_id}", status_code=204)
async def delete_doctor(doctor_id: str, user: dict = Depends(get_current_user)):
    """Delete a doctor record."""
    sb = get_supabase()
    sb.table("doctors").delete().eq("id", doctor_id).execute()
    return None
