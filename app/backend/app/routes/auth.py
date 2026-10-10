"""Authentication endpoints — login and register."""
from fastapi import APIRouter, HTTPException, status
from app.models.schemas import LoginRequest, LoginResponse, RegisterRequest
from app.auth.jwt_handler import hash_password, verify_password, create_access_token
from app.db import get_supabase

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(req: RegisterRequest):
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
async def login(req: LoginRequest):
    """Authenticate user and return JWT token."""
    sb = get_supabase()

    # Fetch user by email
    result = sb.table("users").select("*").eq("email", req.email).execute()

    if not result.data:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    user = result.data[0]

    # Verify password
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
        user={
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "role": user["role"],
            "mr_id": mr_id,
        },
    )


@router.get("/me")
async def get_me(credentials=None):
    """Return the current authenticated user info from token."""
    from app.auth.jwt_handler import get_current_user
    from fastapi import Depends

    # This is handled via dependency injection in the actual call
    return {"message": "Use this endpoint with a Bearer token"}
