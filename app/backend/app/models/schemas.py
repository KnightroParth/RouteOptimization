"""Pydantic schemas for request/response validation."""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date, time, datetime
from enum import Enum


# ── Enums ──────────────────────────────────────────────────────────────
class UserRole(str, Enum):
    MR = "mr"
    MANAGER = "manager"
    ADMIN = "admin"


class VisitStatus(str, Enum):
    PLANNED = "planned"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    MISSED = "missed"


class PriorityClass(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class SolverStatus(str, Enum):
    SUCCESS = "success"
    INFEASIBLE = "infeasible"
    TIMEOUT = "timeout"
    ERROR = "error"


# ── Auth ───────────────────────────────────────────────────────────────
class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict


class RegisterRequest(BaseModel):
    email: str
    password: str = Field(min_length=6)
    name: str
    role: UserRole = UserRole.MR


# ── Doctor ─────────────────────────────────────────────────────────────
class DoctorBase(BaseModel):
    name: str
    specialization: str
    territory: str
    latitude: float
    longitude: float
    availability_start: str  # "09:00"
    availability_end: str    # "17:00"
    typical_visit_duration: int = 30  # minutes
    priority_category: Optional[PriorityClass] = None
    phone: Optional[str] = None
    address: Optional[str] = None


class DoctorCreate(DoctorBase):
    pass


class DoctorResponse(DoctorBase):
    id: str
    created_at: Optional[str] = None


# ── Medical Representative ─────────────────────────────────────────────
class MRBase(BaseModel):
    territory: str
    working_start: str = "09:00"
    working_end: str = "18:00"
    start_lat: float
    start_lng: float
    end_lat: Optional[float] = None
    end_lng: Optional[float] = None


class MRResponse(MRBase):
    id: str
    user_id: str
    name: Optional[str] = None


# ── Visit ──────────────────────────────────────────────────────────────
class VisitCreate(BaseModel):
    doctor_id: str
    mr_id: str
    visit_date: str
    planned_time: Optional[str] = None
    follow_up_required: bool = False


class VisitResponse(BaseModel):
    id: str
    doctor_id: str
    mr_id: str
    visit_date: str
    planned_time: Optional[str] = None
    actual_arrival: Optional[str] = None
    actual_departure: Optional[str] = None
    status: VisitStatus = VisitStatus.PLANNED
    outcome: Optional[str] = None
    follow_up_required: bool = False
    created_at: Optional[str] = None
    # Joined fields
    doctor_name: Optional[str] = None
    doctor_specialization: Optional[str] = None
    doctor_latitude: Optional[float] = None
    doctor_longitude: Optional[float] = None
    priority_class: Optional[str] = None
    priority_score: Optional[float] = None


class VisitStatusUpdate(BaseModel):
    status: VisitStatus
    outcome: Optional[str] = None
    actual_arrival: Optional[str] = None
    actual_departure: Optional[str] = None


# ── Priority Prediction ───────────────────────────────────────────────
class PriorityRequest(BaseModel):
    visit_ids: Optional[List[str]] = None
    mr_id: Optional[str] = None
    date: Optional[str] = None


class PriorityPrediction(BaseModel):
    visit_id: str
    doctor_id: str
    priority_class: PriorityClass
    priority_score: float
    model_version: str


# ── Route ──────────────────────────────────────────────────────────────
class RouteGenerateRequest(BaseModel):
    mr_id: str
    plan_date: str
    visit_ids: Optional[List[str]] = None


class RouteStop(BaseModel):
    sequence_number: int
    doctor_id: str
    doctor_name: Optional[str] = None
    latitude: float
    longitude: float
    estimated_arrival: Optional[str] = None
    estimated_departure: Optional[str] = None
    travel_time_minutes: Optional[float] = None
    service_duration: int = 30
    priority_class: Optional[str] = None
    priority_score: Optional[float] = None


class RouteResponse(BaseModel):
    id: Optional[str] = None
    mr_id: str
    plan_date: str
    solver_status: SolverStatus
    total_travel_time: Optional[float] = None
    total_distance_km: Optional[float] = None
    stops: List[RouteStop] = []
    route_polyline: Optional[List[List[float]]] = None
    generated_at: Optional[str] = None
    message: Optional[str] = None


# ── Dashboard ──────────────────────────────────────────────────────────
class MRDashboardStats(BaseModel):
    total_visits: int = 0
    completed_visits: int = 0
    pending_visits: int = 0
    high_priority_visits: int = 0
    in_progress_visits: int = 0
    completion_rate: float = 0.0


class ManagerDashboardStats(BaseModel):
    total_mrs: int = 0
    total_planned_visits: int = 0
    total_completed: int = 0
    total_pending: int = 0
    high_priority_count: int = 0
    overall_completion_rate: float = 0.0
    mr_summaries: List[dict] = []
