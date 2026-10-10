"""Route generation and retrieval endpoints."""
from fastapi import APIRouter, HTTPException, Depends
from app.models.schemas import RouteGenerateRequest, RouteResponse
from app.auth.jwt_handler import get_current_user
from app.services.priority import predict_batch
from app.services.optimizer import optimize_route
from app.db import get_supabase
from datetime import datetime

router = APIRouter()


@router.post("/generate", response_model=RouteResponse)
async def generate_route(req: RouteGenerateRequest, user: dict = Depends(get_current_user)):
    """
    Generate an optimized daily route for an MR.
    Steps: fetch visits → predict priorities → build matrix → solve VRPTW → store result.
    """
    sb = get_supabase()

    # 1. Get MR profile
    mr_result = (
        sb.table("medical_representatives")
        .select("*")
        .eq("id", req.mr_id)
        .execute()
    )
    if not mr_result.data:
        raise HTTPException(status_code=404, detail="MR not found")
    mr = mr_result.data[0]

    # 2. Fetch visits for the date
    visit_query = (
        sb.table("visits")
        .select("*, doctors(id, name, specialization, latitude, longitude, availability_start, availability_end, typical_visit_duration, priority_category)")
        .eq("mr_id", req.mr_id)
        .eq("visit_date", req.plan_date)
    )
    if req.visit_ids:
        visit_query = visit_query.in_("id", req.visit_ids)

    visit_result = visit_query.execute()

    if not visit_result.data:
        return RouteResponse(
            mr_id=req.mr_id,
            plan_date=req.plan_date,
            solver_status="error",
            message="No visits found for the given date and MR",
        )

    # 3. Flatten visit data and predict priorities
    visits_for_prediction = []
    for v in visit_result.data:
        doctor = v.get("doctors") or {}
        visit_enriched = {
            "id": v["id"],
            "visit_id": v["id"],
            "doctor_id": doctor.get("id") or v.get("doctor_id"),
            "doctor_name": doctor.get("name"),
            "doctor_specialization": doctor.get("specialization"),
            "latitude": doctor.get("latitude"),
            "longitude": doctor.get("longitude"),
            "availability_start": doctor.get("availability_start", "09:00"),
            "availability_end": doctor.get("availability_end", "18:00"),
            "typical_visit_duration": doctor.get("typical_visit_duration", 30),
            "priority_category": doctor.get("priority_category"),
            "follow_up_required": v.get("follow_up_required", False),
            "days_since_last_visit": 30,  # TODO: compute from history
            "visit_frequency": 2,
        }
        visits_for_prediction.append(visit_enriched)

    # 4. Predict priorities
    predictions = predict_batch(visits_for_prediction)

    # Store predictions and enrich visits
    for visit, pred in zip(visits_for_prediction, predictions):
        visit["priority_class"] = pred["priority_class"]
        visit["priority_score"] = pred["priority_score"]

        # Save prediction to DB
        try:
            sb.table("priority_predictions").insert({
                "visit_id": visit["id"],
                "priority_class": pred["priority_class"],
                "priority_score": pred["priority_score"],
                "model_version": pred["model_version"],
            }).execute()
        except Exception:
            pass  # Don't fail route gen if prediction storage fails

    # 5. Run optimizer
    route_result = await optimize_route(
        mr_start=(mr.get("start_lat", 18.5204), mr.get("start_lng", 73.8567)),
        mr_end=(mr.get("end_lat") or mr.get("start_lat", 18.5204),
                mr.get("end_lng") or mr.get("start_lng", 73.8567)),
        visits=visits_for_prediction,
        working_start=mr.get("working_start", "09:00"),
        working_end=mr.get("working_end", "18:00"),
    )

    # 6. Store route in DB
    route_record = {
        "mr_id": req.mr_id,
        "plan_date": req.plan_date,
        "solver_status": route_result["solver_status"],
        "total_travel_time": route_result.get("total_travel_time"),
        "total_distance": route_result.get("total_distance_km"),
    }
    try:
        route_db = sb.table("routes").insert(route_record).execute()
        route_id = route_db.data[0]["id"] if route_db.data else None

        # Store route stops
        if route_id and route_result.get("stops"):
            for stop in route_result["stops"]:
                sb.table("route_stops").insert({
                    "route_id": route_id,
                    "doctor_id": stop["doctor_id"],
                    "sequence_number": stop["sequence_number"],
                    "estimated_arrival": stop.get("estimated_arrival"),
                    "estimated_departure": stop.get("estimated_departure"),
                    "travel_time": stop.get("travel_time_minutes"),
                    "service_duration": stop.get("service_duration", 30),
                }).execute()
    except Exception as e:
        route_id = None
        print(f"Failed to save route: {e}")

    return RouteResponse(
        id=route_id,
        mr_id=req.mr_id,
        plan_date=req.plan_date,
        solver_status=route_result["solver_status"],
        total_travel_time=route_result.get("total_travel_time"),
        total_distance_km=route_result.get("total_distance_km"),
        stops=route_result.get("stops", []),
        route_polyline=route_result.get("route_polyline"),
        generated_at=route_result.get("generated_at"),
        message=route_result.get("message"),
    )


@router.get("/{route_id}")
async def get_route(route_id: str, user: dict = Depends(get_current_user)):
    """Retrieve a specific route with its stops."""
    sb = get_supabase()

    route = sb.table("routes").select("*").eq("id", route_id).execute()
    if not route.data:
        raise HTTPException(status_code=404, detail="Route not found")

    stops = (
        sb.table("route_stops")
        .select("*, doctors(name, latitude, longitude)")
        .eq("route_id", route_id)
        .order("sequence_number")
        .execute()
    )

    route_data = route.data[0]
    route_data["stops"] = []
    for s in stops.data or []:
        doctor = s.pop("doctors", None) or {}
        s["doctor_name"] = doctor.get("name")
        s["latitude"] = doctor.get("latitude")
        s["longitude"] = doctor.get("longitude")
        route_data["stops"].append(s)

    return route_data


@router.get("/")
async def list_routes(
    mr_id: str = None,
    plan_date: str = None,
    user: dict = Depends(get_current_user),
):
    """List routes with optional MR and date filters."""
    sb = get_supabase()
    query = sb.table("routes").select("*")

    if mr_id:
        query = query.eq("mr_id", mr_id)
    if plan_date:
        query = query.eq("plan_date", plan_date)

    result = query.order("generated_at", desc=True).execute()
    return {"routes": result.data or []}
