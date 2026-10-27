"""Doctor management endpoints."""
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional
from app.models.schemas import DoctorCreate, DoctorResponse, DoctorUpdate
from app.auth.jwt_handler import get_current_user
from app.db import get_supabase, is_db_reachable

router = APIRouter()


@router.get("/")
async def list_doctors(
    territory: Optional[str] = Query(None),
    specialization: Optional[str] = Query(None),
    search: Optional[str] = Query(None, description="Search by doctor name"),
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(50, ge=1, le=200, description="Results per page"),
    user: dict = Depends(get_current_user),
):
    """List doctors with optional filtering, search, and pagination."""
    try:
        sb = get_supabase()

        # Count query (for pagination metadata)
        count_query = sb.table("doctors").select("id", count="exact")
        # Data query
        data_query = sb.table("doctors").select("*")

        if territory:
            count_query = count_query.eq("territory", territory)
            data_query = data_query.eq("territory", territory)
        if specialization:
            count_query = count_query.eq("specialization", specialization)
            data_query = data_query.eq("specialization", specialization)
        if search:
            count_query = count_query.ilike("name", f"%{search}%")
            data_query = data_query.ilike("name", f"%{search}%")

        # Get total count
        count_result = count_query.execute()
        total = count_result.count if count_result.count is not None else len(count_result.data or [])

        # Apply pagination
        offset = (page - 1) * limit
        data_query = data_query.order("name").range(offset, offset + limit - 1)
        result = data_query.execute()

        doctors_data = result.data or []
        for d in doctors_data:
            if not d.get("doc_code") and d.get("id"):
                clean = str(d["id"]).replace("-", "")[:6].upper()
                d["doc_code"] = f"DOC-{clean}"

        return {
            "doctors": doctors_data,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": max(1, (total + limit - 1) // limit),
        }
    except Exception:
        # Offline/demo fallback when external Supabase database is unreachable
        from app.services.fallback_data import FALLBACK_DOCTORS
        filtered = FALLBACK_DOCTORS
        if territory:
            filtered = [d for d in filtered if d["territory"].lower() == territory.lower()]
        if specialization:
            filtered = [d for d in filtered if d["specialization"].lower() == specialization.lower()]
        if search:
            filtered = [d for d in filtered if search.lower() in d["name"].lower()]
        total = len(filtered)
        offset = (page - 1) * limit
        paginated = filtered[offset : offset + limit]
        for d in paginated:
            if not d.get("doc_code") and d.get("id"):
                clean = str(d["id"]).replace("-", "")[:6].upper()
                d["doc_code"] = f"DOC-{clean}"
        return {
            "doctors": paginated,
            "total": total,
            "page": page,
            "limit": limit,
            "pages": max(1, (total + limit - 1) // limit),
        }


@router.get("/{doctor_id}")
async def get_doctor(doctor_id: str, user: dict = Depends(get_current_user)):
    """Get a single doctor by ID."""
    sb = get_supabase()
    result = sb.table("doctors").select("*").eq("id", doctor_id).execute()

    if not result.data:
        raise HTTPException(status_code=404, detail="Doctor not found")
    doc = result.data[0]
    if not doc.get("doc_code") and doc.get("id"):
        clean = str(doc["id"]).replace("-", "")[:6].upper()
        doc["doc_code"] = f"DOC-{clean}"
    return doc


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
