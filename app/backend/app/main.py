"""
MR Route Optimization — FastAPI Backend
AI-Based Medical Representative Visit Prioritization and Route Optimization System
"""
import logging
import time
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from dotenv import load_dotenv
from app.db import get_supabase
import os

load_dotenv()

# ── Structured Logging ──────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("mr_route_api")

# ── Rate Limiting ───────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

app = FastAPI(
    title="MR Route Optimization API",
    description="AI-Based Medical Representative Visit Prioritization and Route Optimization System",
    version="0.1.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS
origins = [
    origin.strip()
    for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
    if origin.strip()
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


# ── Request Logging Middleware ──────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration_ms = (time.perf_counter() - start) * 1000
    # Skip health check noise
    if request.url.path not in ("/api/health", "/api/ready"):
        logger.info(
            "%s %s → %d (%.1fms)",
            request.method, request.url.path,
            response.status_code, duration_ms,
        )
    return response


# Import and register routers
from app.routes import auth, doctors, visits, routes as route_routes, dashboard, whatsapp, ml, settings, staff, analytics

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(doctors.router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(visits.router, prefix="/api/visits", tags=["Visits"])
app.include_router(route_routes.router, prefix="/api/routes", tags=["Routes"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(whatsapp.router, prefix="/api/whatsapp", tags=["WhatsApp"])
app.include_router(ml.router, prefix="/api/ml", tags=["ML Predictions"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(staff.router, prefix="/api/staff", tags=["Staff Management"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["Analytics"])


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}


@app.get("/api/ready")
async def readiness_check():
    """Verify that the API process and database dependency can serve traffic."""
    try:
        get_supabase().table("users").select("id").limit(1).execute()
    except Exception as exc:
        return JSONResponse(
            status_code=503,
            content={"status": "not_ready", "database": "unavailable"},
        )
    return {"status": "ready", "database": "ready"}
