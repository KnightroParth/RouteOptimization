"""
MR Route Optimization — FastAPI Backend
AI-Based Medical Representative Visit Prioritization and Route Optimization System
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(
    title="MR Route Optimization API",
    description="AI-Based Medical Representative Visit Prioritization and Route Optimization System",
    version="0.1.0",
)

# CORS
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and register routers
from app.routes import auth, doctors, visits, routes as route_routes, dashboard, whatsapp, ml, settings, staff

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(doctors.router, prefix="/api/doctors", tags=["Doctors"])
app.include_router(visits.router, prefix="/api/visits", tags=["Visits"])
app.include_router(route_routes.router, prefix="/api/routes", tags=["Routes"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(whatsapp.router, prefix="/api/whatsapp", tags=["WhatsApp"])
app.include_router(ml.router, prefix="/api/ml", tags=["ML Predictions"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])
app.include_router(staff.router, prefix="/api/staff", tags=["Staff Management"])


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "version": "0.1.0"}
