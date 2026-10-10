"""
Route Optimization Service — Google OR-Tools VRPTW solver with
OpenRouteService distance/time matrix.
"""
import os
import math
import httpx
from typing import List, Optional, Tuple
from datetime import datetime
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
from dotenv import load_dotenv

load_dotenv()

ORS_API_KEY = os.getenv("ORS_API_KEY", "")
ORS_BASE_URL = "https://api.openrouteservice.org"


def _time_to_minutes(t: str) -> int:
    """Convert 'HH:MM' string to minutes since midnight."""
    parts = t.split(":")
    return int(parts[0]) * 60 + int(parts[1])


def _minutes_to_time(m: int) -> str:
    """Convert minutes since midnight to 'HH:MM' string."""
    return f"{m // 60:02d}:{m % 60:02d}"


def _haversine_distance(lat1, lon1, lat2, lon2) -> float:
    """Calculate haversine distance in km between two points."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _estimate_travel_minutes(dist_km: float, avg_speed_kmh: float = 25.0) -> int:
    """Estimate travel time in minutes from distance (city driving ~25 km/h)."""
    return max(1, int((dist_km / avg_speed_kmh) * 60))


def _build_haversine_matrix(coordinates):
    """Build time and distance matrices using haversine formula."""
    n = len(coordinates)
    time_matrix = []
    dist_matrix = []
    for i in range(n):
        time_row = []
        dist_row = []
        for j in range(n):
            if i == j:
                time_row.append(0)
                dist_row.append(0.0)
            else:
                # coordinates are [lng, lat], so lat=index 1, lng=index 0
                d = _haversine_distance(
                    coordinates[i][1], coordinates[i][0],
                    coordinates[j][1], coordinates[j][0],
                )
                dist_row.append(round(d, 2))
                time_row.append(_estimate_travel_minutes(d))
        time_matrix.append(time_row)
        dist_matrix.append(dist_row)
    return time_matrix, dist_matrix


async def get_ors_matrix(
    coordinates: List[List[float]],
) -> Tuple[List[List[int]], List[List[float]]]:
    """
    Get a time and distance matrix from OpenRouteService.
    Falls back to haversine if API key is unavailable.

    Args:
        coordinates: List of [longitude, latitude] pairs (ORS uses lng,lat order!)

    Returns:
        (time_matrix_minutes, distance_matrix_km)
    """
    # If no API key, use haversine fallback
    if not ORS_API_KEY or ORS_API_KEY == "paste_your_ors_key_here":
        return _build_haversine_matrix(coordinates)

    # Call ORS Matrix API
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(
                f"{ORS_BASE_URL}/v2/matrix/driving-car",
                headers={
                    "Authorization": ORS_API_KEY,
                    "Content-Type": "application/json",
                },
                json={
                    "locations": coordinates,
                    "metrics": ["duration", "distance"],
                    "units": "km",
                },
            )
            resp.raise_for_status()
            data = resp.json()

            # Convert durations from seconds to minutes
            time_matrix = [
                [max(1, int(cell / 60)) if cell else 0 for cell in row]
                for row in data["durations"]
            ]
            dist_matrix = [
                [round(cell, 2) if cell else 0.0 for cell in row]
                for row in data["distances"]
            ]
            return time_matrix, dist_matrix

    except Exception as e:
        print(f"ORS API error, falling back to haversine: {e}")
        return _build_haversine_matrix(coordinates)


async def optimize_route(
    mr_start: Tuple[float, float],  # (lat, lng)
    mr_end: Optional[Tuple[float, float]],  # (lat, lng) or None = same as start
    visits: List[dict],  # Each has lat, lng, availability_start/end, duration, priority_score
    working_start: str = "09:00",
    working_end: str = "18:00",
) -> dict:
    """
    Solve VRPTW for a single MR's daily route.

    Args:
        mr_start: MR start location (lat, lng)
        mr_end: MR end location (defaults to start)
        visits: List of visit dicts with location and constraint data
        working_start: MR working day start
        working_end: MR working day end

    Returns:
        dict with solver_status, stops, total_travel_time, total_distance, route_polyline
    """
    if not visits:
        return {
            "solver_status": "error",
            "message": "No visits provided for route optimization",
            "stops": [],
        }

    if mr_end is None:
        mr_end = mr_start

    # Build node list: [start, visit_0, visit_1, ..., end]
    nodes = [
        {"lat": mr_start[0], "lng": mr_start[1], "type": "depot_start"},
    ]
    for v in visits:
        nodes.append({
            "lat": v["latitude"],
            "lng": v["longitude"],
            "type": "visit",
            "visit_data": v,
        })
    nodes.append(
        {"lat": mr_end[0], "lng": mr_end[1], "type": "depot_end"},
    )

    n = len(nodes)

    # Build coordinate list for matrix (ORS uses [lng, lat])
    coordinates = [[node["lng"], node["lat"]] for node in nodes]

    # Get distance/time matrix
    time_matrix, dist_matrix = await get_ors_matrix(coordinates)

    # Working hours as minutes since midnight
    work_start = _time_to_minutes(working_start)
    work_end = _time_to_minutes(working_end)

    # Build time windows for each node
    time_windows = []
    service_times = []
    for i, node in enumerate(nodes):
        if node["type"] in ("depot_start", "depot_end"):
            time_windows.append((work_start, work_end))
            service_times.append(0)
        else:
            vd = node["visit_data"]
            avail_start = _time_to_minutes(vd.get("availability_start", working_start))
            avail_end = _time_to_minutes(vd.get("availability_end", working_end))
            # Clamp to working hours
            tw_start = max(work_start, avail_start)
            tw_end = min(work_end, avail_end)
            time_windows.append((tw_start, tw_end))
            service_times.append(vd.get("typical_visit_duration", 30))

    # --- OR-Tools VRPTW Setup ---
    manager = pywrapcp.RoutingIndexManager(n, 1, [0], [n - 1])
    routing = pywrapcp.RoutingModel(manager)

    # Travel time callback
    def time_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return time_matrix[from_node][to_node] + service_times[from_node]

    transit_callback_index = routing.RegisterTransitCallback(time_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Time dimension
    routing.AddDimension(
        transit_callback_index,
        120,  # max waiting time (minutes)
        3000,  # max capacity (minutes since midnight)
        False,
        "Time",
    )
    time_dimension = routing.GetDimensionOrDie("Time")

    # Add time windows
    for i in range(n):
        if i == 0:
            index = manager.GetStartIndex(0)
        elif i == n - 1:
            index = manager.GetEndIndex(0)
        else:
            index = manager.NodeToIndex(i)
            
        time_dimension.CumulVar(index).SetRange(
            time_windows[i][0], time_windows[i][1]
        )

    # Allow dropping visits with a penalty (priority-weighted)
    for i in range(1, n - 1):
        visit_data = nodes[i].get("visit_data", {})
        priority_score = visit_data.get("priority_score", 0.5)
        # Higher priority → higher penalty for dropping
        penalty = int(1000 + priority_score * 2000)
        routing.AddDisjunction([manager.NodeToIndex(i)], penalty)

    # Search parameters
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_params.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    )
    search_params.time_limit.seconds = 10  # 10-second limit for prototype

    # Solve
    solution = routing.SolveWithParameters(search_params)

    if not solution:
        return {
            "solver_status": "infeasible",
            "message": "No feasible route found for the given constraints. Try relaxing time windows or reducing visits.",
            "stops": [],
            "total_travel_time": None,
            "total_distance_km": None,
        }

    # Extract solution
    stops = []
    route_coords = []
    index = routing.Start(0)
    total_time = 0
    total_dist = 0
    seq = 0
    prev_node_idx = 0  # Track previous node for travel time calc

    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        time_var = time_dimension.CumulVar(index)
        arrival_min = solution.Min(time_var)

        if nodes[node]["type"] == "visit":
            vd = nodes[node]["visit_data"]
            travel_from_prev = time_matrix[prev_node_idx][node]

            stops.append({
                "sequence_number": seq + 1,
                "doctor_id": vd.get("doctor_id") or vd.get("id"),
                "doctor_name": vd.get("doctor_name") or vd.get("name"),
                "latitude": nodes[node]["lat"],
                "longitude": nodes[node]["lng"],
                "estimated_arrival": _minutes_to_time(arrival_min),
                "estimated_departure": _minutes_to_time(arrival_min + service_times[node]),
                "travel_time_minutes": travel_from_prev,
                "service_duration": service_times[node],
                "priority_class": vd.get("priority_class"),
                "priority_score": vd.get("priority_score"),
            })
            seq += 1

        route_coords.append([nodes[node]["lat"], nodes[node]["lng"]])
        prev_node_idx = node
        prev_index = index
        index = solution.Value(routing.NextVar(index))

        # Accumulate travel info
        from_node = manager.IndexToNode(prev_index)
        to_node = manager.IndexToNode(index)
        if to_node < n:
            total_time += time_matrix[from_node][to_node]
            total_dist += dist_matrix[from_node][to_node]

    # Add end depot to polyline
    end_node = manager.IndexToNode(index)
    route_coords.append([nodes[end_node]["lat"], nodes[end_node]["lng"]])

    return {
        "solver_status": "success",
        "stops": stops,
        "total_travel_time": round(total_time, 1),
        "total_distance_km": round(total_dist, 2),
        "route_polyline": route_coords,
        "generated_at": datetime.utcnow().isoformat(),
        "message": f"Optimized route with {len(stops)} stops",
    }
