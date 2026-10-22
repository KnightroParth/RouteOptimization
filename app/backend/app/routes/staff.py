"""Staff management endpoints — manager-only CRUD for MR users."""
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import Optional
from app.auth.jwt_handler import hash_password, get_current_user
from app.db import get_supabase

router = APIRouter()


class CreateStaffRequest(BaseModel):
    name: str
    email: str
    password: str
    territory: str
    phone: Optional[str] = None
    working_start: str = "09:00"
    working_end: str = "18:00"
    start_lat: float = 18.5204
    start_lng: float = 73.8567


class UpdateStaffRequest(BaseModel):
    name: Optional[str] = None
    territory: Optional[str] = None
    phone: Optional[str] = None
    working_start: Optional[str] = None
    working_end: Optional[str] = None
    status: Optional[str] = None  # "active" | "inactive"


def require_manager(user=Depends(get_current_user)):
    if user.get("role") != "manager":
        raise HTTPException(status_code=403, detail="Manager access required")
    return user


@router.get("/")
async def list_staff(user=Depends(require_manager)):
    """List all MR users with their profile data."""
    sb = get_supabase()

    users_res = sb.table("users").select("id, name, email, role, created_at").eq("role", "mr").execute()
    users = users_res.data or []

    mrs_res = sb.table("medical_representatives").select("id, user_id, territory, working_start, working_end, start_lat, start_lng").execute()
    mrs_map = {mr["user_id"]: mr for mr in (mrs_res.data or [])}

    staff = []
    for u in users:
        mr_profile = mrs_map.get(u["id"], {})
        staff.append({
            "user_id": u["id"],
            "mr_id": mr_profile.get("id"),
            "name": u["name"],
            "email": u["email"],
            "role": u["role"],
            "territory": mr_profile.get("territory", "Unassigned"),
            "working_start": mr_profile.get("working_start", "09:00"),
            "working_end": mr_profile.get("working_end", "18:00"),
            "created_at": u.get("created_at"),
            "status": "active",
        })

    return {"staff": staff, "total": len(staff)}


@router.post("/", status_code=201)
async def create_staff(req: CreateStaffRequest, user=Depends(require_manager)):
    """Create a new MR user with profile."""
    sb = get_supabase()

    existing = sb.table("users").select("id").eq("email", req.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    user_data = {
        "email": req.email,
        "password_hash": hash_password(req.password),
        "name": req.name,
        "role": "mr",
    }
    user_res = sb.table("users").insert(user_data).execute()
    if not user_res.data:
        raise HTTPException(status_code=500, detail="Failed to create user")

    new_user = user_res.data[0]

    mr_data = {
        "user_id": new_user["id"],
        "territory": req.territory,
        "working_start": req.working_start,
        "working_end": req.working_end,
        "start_lat": req.start_lat,
        "start_lng": req.start_lng,
        "end_lat": req.start_lat,
        "end_lng": req.start_lng,
    }
    mr_res = sb.table("medical_representatives").insert(mr_data).execute()
    mr_id = mr_res.data[0]["id"] if mr_res.data else None

    return {
        "message": "Staff member created successfully",
        "user_id": new_user["id"],
        "mr_id": mr_id,
        "name": req.name,
        "email": req.email,
        "territory": req.territory,
    }


@router.patch("/{user_id}")
async def update_staff(user_id: str, req: UpdateStaffRequest, user=Depends(require_manager)):
    """Update an MR's name and/or territory/hours."""
    sb = get_supabase()

    # Update user name if provided
    if req.name:
        sb.table("users").update({"name": req.name}).eq("id", user_id).execute()

    # Update MR profile fields
    mr_updates = {}
    if req.territory:
        mr_updates["territory"] = req.territory
    if req.working_start:
        mr_updates["working_start"] = req.working_start
    if req.working_end:
        mr_updates["working_end"] = req.working_end

    if mr_updates:
        sb.table("medical_representatives").update(mr_updates).eq("user_id", user_id).execute()

    return {"message": "Staff member updated successfully", "user_id": user_id}


@router.delete("/{user_id}", status_code=200)
async def delete_staff(user_id: str, user=Depends(require_manager)):
    """Remove an MR user and their profile."""
    sb = get_supabase()

    # Check user exists and is MR
    check = sb.table("users").select("id, role").eq("id", user_id).execute()
    if not check.data:
        raise HTTPException(status_code=404, detail="User not found")
    if check.data[0].get("role") != "mr":
        raise HTTPException(status_code=400, detail="Can only remove MR users")

    # Delete MR profile first (FK constraint)
    sb.table("medical_representatives").delete().eq("user_id", user_id).execute()
    # Delete user
    sb.table("users").delete().eq("id", user_id).execute()

    return {"message": "Staff member removed successfully", "user_id": user_id}
