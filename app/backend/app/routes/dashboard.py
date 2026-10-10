"""Dashboard data endpoints for MR and Manager views."""
from fastapi import APIRouter, Depends, Query
from app.auth.jwt_handler import get_current_user, require_role
from app.db import get_supabase

router = APIRouter()


@router.get("/mr")
async def mr_dashboard(
    mr_id: str = Query(...),
    date: str = Query(None),
    user: dict = Depends(get_current_user),
):
    """Get MR dashboard stats: total, completed, pending, high-priority visits."""
    sb = get_supabase()

    query = sb.table("visits").select("id, status, follow_up_required").eq("mr_id", mr_id)
    if date:
        query = query.eq("visit_date", date)

    result = query.execute()
    visits = result.data or []

    total = len(visits)
    completed = sum(1 for v in visits if v["status"] == "completed")
    in_progress = sum(1 for v in visits if v["status"] == "in_progress")
    pending = sum(1 for v in visits if v["status"] == "planned")
    cancelled = sum(1 for v in visits if v["status"] in ("cancelled", "missed"))

    # Count high-priority visits
    visit_ids = [v["id"] for v in visits]
    high_priority = 0
    if visit_ids:
        pred_result = (
            sb.table("priority_predictions")
            .select("visit_id, priority_class")
            .in_("visit_id", visit_ids)
            .eq("priority_class", "high")
            .execute()
        )
        high_priority = len(set(p["visit_id"] for p in pred_result.data or []))

    completion_rate = round((completed / total * 100), 1) if total > 0 else 0.0

    return {
        "total_visits": total,
        "completed_visits": completed,
        "in_progress_visits": in_progress,
        "pending_visits": pending,
        "cancelled_visits": cancelled,
        "high_priority_visits": high_priority,
        "completion_rate": completion_rate,
    }


@router.get("/manager")
async def manager_dashboard(user: dict = Depends(require_role("manager", "admin"))):
    """Get manager dashboard: aggregate stats across all MRs."""
    sb = get_supabase()

    # Get all MRs
    mrs = sb.table("medical_representatives").select("id, user_id, territory").execute()
    mr_list = mrs.data or []

    # Get user names
    user_ids = [m["user_id"] for m in mr_list]
    users = {}
    if user_ids:
        user_result = sb.table("users").select("id, name").in_("id", user_ids).execute()
        users = {u["id"]: u["name"] for u in user_result.data or []}

    # Get all visits
    all_visits = sb.table("visits").select("id, mr_id, status").execute()
    visits = all_visits.data or []

    total_planned = len(visits)
    total_completed = sum(1 for v in visits if v["status"] == "completed")
    total_pending = sum(1 for v in visits if v["status"] == "planned")

    # High priority count
    visit_ids = [v["id"] for v in visits]
    high_count = 0
    if visit_ids:
        hp = (
            sb.table("priority_predictions")
            .select("visit_id")
            .in_("visit_id", visit_ids)
            .eq("priority_class", "high")
            .execute()
        )
        high_count = len(set(p["visit_id"] for p in hp.data or []))

    # Per-MR summaries
    mr_summaries = []
    for m in mr_list:
        mr_visits = [v for v in visits if v["mr_id"] == m["id"]]
        mr_total = len(mr_visits)
        mr_completed = sum(1 for v in mr_visits if v["status"] == "completed")
        mr_summaries.append({
            "mr_id": m["id"],
            "name": users.get(m["user_id"], "Unknown"),
            "territory": m["territory"],
            "total_visits": mr_total,
            "completed": mr_completed,
            "pending": mr_total - mr_completed,
            "completion_rate": round((mr_completed / mr_total * 100), 1) if mr_total > 0 else 0.0,
        })

    return {
        "total_mrs": len(mr_list),
        "total_planned_visits": total_planned,
        "total_completed": total_completed,
        "total_pending": total_pending,
        "high_priority_count": high_count,
        "overall_completion_rate": round((total_completed / total_planned * 100), 1) if total_planned > 0 else 0.0,
        "mr_summaries": mr_summaries,
    }
