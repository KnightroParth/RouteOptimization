"""
WhatsApp Service for MR Route Optimization.
Supports:
1. Zero-verification Direct WhatsApp (wa.me link generator for instant mobile messaging)
2. Sandbox / Test Number Automation (Twilio WhatsApp Sandbox test number +14155238886 or simulated test webhook)
3. Audit log of automated notifications
"""
import os
import urllib.parse
from datetime import datetime, timezone
from typing import Optional, Dict, List
import httpx
from dotenv import load_dotenv

load_dotenv()

# Optional Twilio Sandbox configuration (test-only, no business verification needed)
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN", "")
TWILIO_SANDBOX_NUMBER = os.getenv("TWILIO_SANDBOX_NUMBER", "whatsapp:+14155238886")
DEFAULT_TEST_RECIPIENT = os.getenv("WHATSAPP_TEST_RECIPIENT", "+919876543210")

# In-memory notification log for sandbox / test runs
TEST_NOTIFICATION_LOG: List[Dict] = []


def _clean_phone(phone_number: str) -> str:
    clean_phone = "".join(filter(str.isdigit, phone_number or ""))
    if not 8 <= len(clean_phone) <= 15:
        raise ValueError("Phone number must contain 8 to 15 digits")
    return clean_phone


def generate_direct_whatsapp_url(phone_number: str, message: str) -> str:
    """
    Generate a direct wa.me link that opens WhatsApp directly without any API or verification.
    Strikes all spaces/symbols from phone number.
    """
    clean_phone = _clean_phone(phone_number)
    if not message or not message.strip():
        raise ValueError("Message cannot be empty")
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{clean_phone}?text={encoded_message}"


def get_message_templates(
    doctor_name: str = "Doctor",
    mr_name: str = "Medical Representative",
    time_str: str = "11:30 AM",
    date_str: Optional[str] = None,
    clinic_address: str = "",
    distance_km: Optional[float] = None,
    eta_mins: int = 15,
) -> Dict[str, str]:
    """Get standardized, professional WhatsApp templates for field visits."""
    if not date_str:
        date_str = datetime.now().strftime("%d %b %Y")

    return {
        "on_the_way": (
            f"🩺 *Appointment Update - MedRoute Pharma*\n\n"
            f"Dear Dr. {doctor_name},\n"
            f"This is {mr_name}. I am en route to your clinic/hospital for our scheduled consultation.\n\n"
            f"⏱️ *Estimated Arrival:* In ~{eta_mins} mins ({time_str})\n"
            f"📍 *Location:* {clinic_address or 'Your Clinic'}\n\n"
            f"Thank you for your valuable time!"
        ),
        "confirmation": (
            f"📋 *Visit Confirmation - MedRoute*\n\n"
            f"Dear Dr. {doctor_name},\n"
            f"Confirming our scheduled appointment for *today ({date_str}) at {time_str}*.\n\n"
            f"Agenda: Sharing latest clinical updates, drug monographs & scientific literature.\n\n"
            f"Looking forward to meeting you.\n"
            f"— {mr_name}"
        ),
        "post_visit": (
            f"✅ *Thank You - MedRoute Follow-Up*\n\n"
            f"Dear Dr. {doctor_name},\n"
            f"Thank you for granting me time today ({time_str}).\n\n"
            f"The digital product monographs and dosage cards discussed have been logged. "
            f"Please let me know if you require any specialized trial reprints or further samples.\n\n"
            f"Warm regards,\n"
            f"{mr_name}"
        ),
        "delayed": (
            f"⚠️ *Brief Delay Notice - MedRoute*\n\n"
            f"Dear Dr. {doctor_name},\n"
            f"Due to traffic delay on my current route, my arrival is rescheduled slightly by 15-20 minutes. "
            f"I sincerely apologize for any inconvenience caused and will check in with your desk upon arrival.\n\n"
            f"— {mr_name}"
        ),
        "manager_summary": (
            f"📊 *Daily MR Activity Report*\n\n"
            f"Date: {date_str}\n"
            f"MR: {mr_name}\n\n"
            f"Optimized route followed via MedRoute AI. Distance logged: {distance_km or 0} km.\n"
            f"All planned doctor visits completed/in-progress."
        ),
    }


async def send_sandbox_whatsapp_message(
    to_number: str,
    message: str,
    template_type: str = "custom",
) -> Dict:
    """
    Send via Twilio WhatsApp Sandbox (test-only number) or simulate automated delivery.
    Strictly uses test number, zero business verification needed.
    """
    clean_digits = _clean_phone(to_number.replace("whatsapp:", ""))
    expected_digits = _clean_phone(DEFAULT_TEST_RECIPIENT)
    if clean_digits != expected_digits:
        raise ValueError("Recipient is not the configured test number")
    if not message or not message.strip():
        raise ValueError("Message cannot be empty")

    clean_to = f"whatsapp:{clean_digits}"
    timestamp = datetime.now(timezone.utc).isoformat()

    # If Twilio credentials are configured, send live test message
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
        try:
            url = f"https://api.twilio.com/2010-04-01/Accounts/{TWILIO_ACCOUNT_SID}/Messages.json"
            async with httpx.AsyncClient(timeout=10.0) as client:
                resp = await client.post(
                    url,
                    auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN),
                    data={
                        "From": TWILIO_SANDBOX_NUMBER,
                        "To": clean_to,
                        "Body": message,
                    },
                )
                data = resp.json()
                record = {
                    "id": f"wa_{int(datetime.now(timezone.utc).timestamp())}",
                    "to": clean_to,
                    "body": message,
                    "template": template_type,
                    "status": "sent" if resp.status_code in [200, 201] else "failed",
                    "sent_at": timestamp,
                    "provider": "twilio_sandbox",
                    "response": data,
                }
                TEST_NOTIFICATION_LOG.insert(0, record)
                return record
        except Exception as e:
            record = {
                "id": f"wa_err_{int(datetime.now(timezone.utc).timestamp())}",
                "to": clean_to,
                "body": message,
                "template": template_type,
                "status": "simulation_fallback",
                "error": str(e),
                "sent_at": timestamp,
                "provider": "sandbox_simulator",
            }
            TEST_NOTIFICATION_LOG.insert(0, record)
            return record

    # Pure Sandbox / Test Simulation (Instant & 100% reliable without any API key setup)
    record = {
        "id": f"wa_test_{int(datetime.now(timezone.utc).timestamp())}",
        "to": clean_to,
        "body": message,
        "template": template_type,
        "status": "delivered_sandbox",
        "sent_at": timestamp,
        "provider": "medroute_test_sandbox",
        "note": "Delivered to test sandbox receiver without business verification requirement.",
    }
    TEST_NOTIFICATION_LOG.insert(0, record)
    # Keep log within 50 items
    if len(TEST_NOTIFICATION_LOG) > 50:
        TEST_NOTIFICATION_LOG.pop()

    return record
