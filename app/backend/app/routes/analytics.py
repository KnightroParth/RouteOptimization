"""Analytics endpoints for rich dashboard charts and trend data."""
from fastapi import APIRouter, Depends
from app.auth.jwt_handler import get_current_user, require_role
from app.db import get_supabase
from collections import defaultdict
from datetime import date, timedelta

router = APIRouter()


@router.get("/overview")
async def analytics_overview(user: dict = Depends(require_role("manager", "admin"))):
    """
    Rich analytics overview with:
    - Priority distribution (pie chart)
    - Visit trends over last 30 days (line chart)
    - Specialty coverage breakdown (bar chart)
    - Territory performance comparison (bar chart)
    """
    sb = get_supabase()

    # 1. Priority distribution from predictions
    preds = sb.table("priority_predictions").select("priority_class, visit_id").execute()
    pred_data = preds.data or []
    priority_dist = defaultdict(int)
    seen_visits = set()
    for p in pred_data:
        vid = p["visit_id"]
        if vid not in seen_visits:
            seen_visits.add(vid)
            priority_dist[p["priority_class"]] += 1

    priority_chart = [
        {"name": "High", "value": priority_dist.get("high", 0), "color": "#ef4444"},
        {"name": "Medium", "value": priority_dist.get("medium", 0), "color": "#f59e0b"},
        {"name": "Low", "value": priority_dist.get("low", 0), "color": "#10b981"},
    ]

    # 2. Visit trends over last 30 days
    today = date.today()
    thirty_days_ago = today - timedelta(days=30)
    visits_result = sb.table("visits").select("visit_date, status").gte(
        "visit_date", thirty_days_ago.isoformat()
    ).execute()
    visits = visits_result.data or []

    daily_stats = defaultdict(lambda: {"completed": 0, "planned": 0, "cancelled": 0})
    for v in visits:
        d = v.get("visit_date", "")
        s = v.get("status", "planned")
        if s == "completed":
            daily_stats[d]["completed"] += 1
        elif s in ("cancelled", "missed"):
            daily_stats[d]["cancelled"] += 1
        else:
            daily_stats[d]["planned"] += 1

    visit_trends = []
    for i in range(30):
        d = (thirty_days_ago + timedelta(days=i + 1)).isoformat()
        stats = daily_stats.get(d, {"completed": 0, "planned": 0, "cancelled": 0})
        visit_trends.append({
            "date": d,
            "completed": stats["completed"],
            "planned": stats["planned"],
            "cancelled": stats["cancelled"],
        })

    # 3. Specialty coverage breakdown
    doctors_result = sb.table("doctors").select("id, specialization").execute()
    doctors = doctors_result.data or []
    spec_map = {d["id"]: d.get("specialization", "Unknown") for d in doctors}

    all_visits = sb.table("visits").select("doctor_id, status").execute()
    all_visit_data = all_visits.data or []

    spec_stats = defaultdict(lambda: {"total": 0, "completed": 0})
    for v in all_visit_data:
        spec = spec_map.get(v.get("doctor_id"), "Unknown")
        spec_stats[spec]["total"] += 1
        if v.get("status") == "completed":
            spec_stats[spec]["completed"] += 1

    specialty_chart = sorted(
        [
            {
                "specialty": spec,
                "total_visits": s["total"],
                "completed": s["completed"],
                "completion_rate": round(s["completed"] / s["total"] * 100, 1) if s["total"] > 0 else 0,
            }
            for spec, s in spec_stats.items()
        ],
        key=lambda x: x["total_visits"],
        reverse=True,
    )[:10]  # Top 10 specialties

    # 4. Territory performance
    mrs = sb.table("medical_representatives").select("id, territory, user_id").execute()
    mr_list = mrs.data or []
    mr_territory = {m["id"]: m.get("territory", "Unknown") for m in mr_list}

    territory_stats = defaultdict(lambda: {"total": 0, "completed": 0, "mr_count": 0})
    territory_mrs = defaultdict(set)
    for m in mr_list:
        t = m.get("territory", "Unknown")
        territory_mrs[t].add(m["id"])
        territory_stats[t]["mr_count"] = len(territory_mrs[t])

    for v in all_visit_data:
        t = mr_territory.get(v.get("mr_id"), "Unknown")
        territory_stats[t]["total"] += 1
        if v.get("status") == "completed":
            territory_stats[t]["completed"] += 1

    territory_chart = sorted(
        [
            {
                "territory": t,
                "total_visits": s["total"],
                "completed": s["completed"],
                "mr_count": s["mr_count"],
                "completion_rate": round(s["completed"] / s["total"] * 100, 1) if s["total"] > 0 else 0,
            }
            for t, s in territory_stats.items()
        ],
        key=lambda x: x["total_visits"],
        reverse=True,
    )

    return {
        "priority_distribution": priority_chart,
        "visit_trends": visit_trends,
        "specialty_coverage": specialty_chart,
        "territory_performance": territory_chart,
    }
