"""
Endpoints for WhatsApp notifications strictly using test numbers and direct messaging.
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from typing import Optional, Dict
from app.auth.jwt_handler import get_current_user
from app.services.whatsapp import (
    generate_direct_whatsapp_url,
    get_message_templates,
    send_sandbox_whatsapp_message,
    TEST_NOTIFICATION_LOG,
    DEFAULT_TEST_RECIPIENT,
)

router = APIRouter()


class WhatsAppTestPayload(BaseModel):
    to_number: str = Field(default="+919876543210", description="Strictly test phone number")
    message: str
    template_type: Optional[str] = "custom"


class WhatsAppTemplateRequest(BaseModel):
    doctor_name: Optional[str] = "Dr. Sharma"
    mr_name: Optional[str] = "Medical Rep"
    time_str: Optional[str] = "11:30 AM"
    date_str: Optional[str] = None
    clinic_address: Optional[str] = "Pune Clinic"
    distance_km: Optional[float] = None
    eta_mins: Optional[int] = 15


@router.post("/templates")
async def generate_templates(
    req: WhatsAppTemplateRequest,
    user: dict = Depends(get_current_user),
):
    """Generate ready-to-use WhatsApp templates with current visit data."""
    mr_display_name = user.get("name") or req.mr_name
    templates = get_message_templates(
        doctor_name=req.doctor_name or "Doctor",
        mr_name=mr_display_name,
        time_str=req.time_str or "11:30 AM",
        date_str=req.date_str,
        clinic_address=req.clinic_address or "",
        distance_km=req.distance_km,
        eta_mins=req.eta_mins or 15,
    )
    return {"templates": templates}


@router.get("/direct-link")
async def get_direct_link(
    phone: str = Query(...),
    message: str = Query(...),
    user: dict = Depends(get_current_user),
):
    """Generate direct zero-verification wa.me link."""
    try:
        url = generate_direct_whatsapp_url(phone, message)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"url": url}


@router.post("/send-test")
async def send_test_message(
    payload: WhatsAppTestPayload,
    user: dict = Depends(get_current_user),
):
    """
    Send automated notification to a strictly test phone number without business verification.
    """
    if not payload.message:
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    try:
        result = await send_sandbox_whatsapp_message(
            to_number=payload.to_number,
            message=payload.message,
            template_type=payload.template_type or "custom",
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {
        "success": True,
        "detail": "Test notification processed via test sandbox",
        "record": result,
    }


@router.get("/logs")
async def get_test_logs(user: dict = Depends(get_current_user)):
    """Retrieve history of sent test WhatsApp notifications."""
    return {
        "logs": TEST_NOTIFICATION_LOG,
        "default_test_number": DEFAULT_TEST_RECIPIENT,
        "mode": "test_sandbox_unverified",
    }
