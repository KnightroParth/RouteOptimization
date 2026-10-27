"""Authentication endpoints — login and register."""
from fastapi import APIRouter, Depends, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.models.schemas import LoginRequest, LoginResponse, RegisterRequest
from app.auth.jwt_handler import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.db import get_supabase

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


@router.post("/register", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def register(request: Request, req: RegisterRequest):
    """Register a new user (MR or Manager)."""
    sb = get_supabase()

    # Check if user already exists
    existing = sb.table("users").select("id").eq("email", req.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create user
    user_data = {
        "email": req.email,
        "password_hash": hash_password(req.password),
        "name": req.name,
        "role": req.role.value,
    }
    result = sb.table("users").insert(user_data).execute()

    if not result.data:
        raise HTTPException(status_code=500, detail="Failed to create user")

    user = result.data[0]

    # If MR role, also create MR profile with defaults
    if req.role.value == "mr":
        mr_data = {
            "user_id": user["id"],
            "territory": "Pune",
            "working_start": "09:00",
            "working_end": "18:00",
            "start_lat": 18.5204,
            "start_lng": 73.8567,
            "end_lat": 18.5204,
            "end_lng": 73.8567,
        }
        sb.table("medical_representatives").insert(mr_data).execute()

    return {"message": "User registered successfully", "user_id": user["id"]}


@router.post("/login", response_model=LoginResponse)
@limiter.limit("10/minute")
async def login(request: Request, req: LoginRequest):
    """Authenticate user and return JWT token."""
    sb = get_supabase()

    # 1. Try authenticating against live database
    try:
        result = sb.table("users").select("*").eq("email", req.email).execute()
        if not result.data:
            raise HTTPException(status_code=401, detail="Invalid email or password")
        user = result.data[0]
        if not verify_password(req.password, user["password_hash"]):
            raise HTTPException(status_code=401, detail="Invalid email or password")

        # Fetch MR profile if applicable
        mr_id = None
        if user["role"] == "mr":
            mr_result = (
                sb.table("medical_representatives")
                .select("id")
                .eq("user_id", user["id"])
                .execute()
            )
            if mr_result.data:
                mr_id = mr_result.data[0]["id"]

        # Create JWT
        token = create_access_token(
            {
                "sub": user["id"],
                "email": user["email"],
                "role": user["role"],
                "name": user["name"],
                "mr_id": mr_id,
            }
        )

        return LoginResponse(
            access_token=token,
            token_type="bearer",
            user={
                "id": user["id"],
                "email": user["email"],
                "name": user["name"],
                "role": user["role"],
                "mr_id": mr_id,
            },
        )
    except HTTPException:
        raise
    except Exception as exc:
        # Fallback to demo accounts only if database connection fails
        demo_accounts = {
            "mr@demo.com": {
                "id": "871d5597-1678-4f5a-aa33-0ffca6dcdcbc",
                "name": "Parth Lokhande",
                "role": "mr",
                "mr_id": "e47e41a3-c517-4af7-a6fd-004f908f7185",
            },
            "manager@demo.com": {
                "id": "fde8d462-48dd-4b31-83ee-09c19125d534",
                "name": "Rajesh Mehta",
                "role": "manager",
                "mr_id": None,
            },
            "mr2@demo.com": {
                "id": "6a62ebbd-d8f4-40d9-b6f2-40cdeb7d71dd",
                "name": "Bhakti Gundecha",
                "role": "mr",
                "mr_id": "f00cb353-d292-45b0-a274-9cad4c702110",
            },
            "mr3@demo.com": {
                "id": "0269eb42-e1d8-47ad-a90f-bdb0b1ec3ffa",
                "name": "Udaykiran Bitla",
                "role": "mr",
                "mr_id": "3d9957db-0bdf-440d-8d4b-2985464a3296",
            },
        }
        if req.email in demo_accounts and req.password == "demo123":
            demo_user = demo_accounts[req.email]
            token = create_access_token(
                {
                    "sub": demo_user["id"],
                    "email": req.email,
                    "role": demo_user["role"],
                    "name": demo_user["name"],
                    "mr_id": demo_user["mr_id"],
                }
            )
            return LoginResponse(
                access_token=token,
                token_type="bearer",
                user={
                    "id": demo_user["id"],
                    "email": req.email,
                    "name": demo_user["name"],
                    "role": demo_user["role"],
                    "mr_id": demo_user["mr_id"],
                },
            )
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database temporarily unreachable.",
        )


@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    """Return the current authenticated user's token claims."""
    return {"user": user}
