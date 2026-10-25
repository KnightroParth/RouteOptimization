"""Supabase database client singleton."""
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

DEFAULT_SUPABASE_URL = "https://edvishnlwtostwlcakqz.supabase.co"
DEFAULT_SUPABASE_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVk"
    "dmlzaG5sd3Rvc3R3bGNha3F6Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc5MTUz"
    "NjkzMCwiZXhwIjoyMTA3MTEyOTMwfQ.86HVPl9Ex_0VxEK3XzPwImoVrtZ-ta5iJ2q-hNDpUy0"
)

import time

_supabase: Client | None = None
_db_status: bool | None = None
_last_check_time: float = 0.0


def get_supabase() -> Client:
    """Return a cached Supabase client."""
    global _supabase
    if _supabase is None:
        url = os.getenv("SUPABASE_URL") or DEFAULT_SUPABASE_URL
        key = (
            os.getenv("SUPABASE_SERVICE_KEY")
            or os.getenv("SUPABASE_KEY")
            or DEFAULT_SUPABASE_KEY
        )
        _supabase = create_client(url, key)
    return _supabase


def is_db_reachable() -> bool:
    """Check if the database is reachable, cached for 60 seconds to avoid DNS timeouts."""
    global _db_status, _last_check_time
    now = time.time()
    if _db_status is not None and (now - _last_check_time < 60.0):
        return _db_status
    try:
        sb = get_supabase()
        sb.table("users").select("id").limit(1).execute()
        _db_status = True
    except Exception:
        _db_status = False
    _last_check_time = now
    return _db_status
