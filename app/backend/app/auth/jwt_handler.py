"""JWT authentication utilities."""
import os
from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

load_dotenv()

configured_secret = os.getenv("JWT_SECRET")
DEFAULT_SECRET = "mr-route-optimization-jwt-secret-key-2026-pvgcoet"
SECRET_KEY = configured_secret or DEFAULT_SECRET
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
EXPIRATION = int(os.getenv("JWT_EXPIRATION_MINUTES", "480"))

security = HTTPBearer()


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=EXPIRATION))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> dict:
    """Dependency that extracts and validates the current user from JWT."""
    payload = decode_token(credentials.credentials)
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return {
        "id": user_id,
        "email": payload.get("email", ""),
        "role": payload.get("role", "mr"),
        "name": payload.get("name", ""),
        "mr_id": payload.get("mr_id"),
    }


def require_role(*roles: str):
    """Dependency factory that enforces role-based access."""
    async def role_checker(user: dict = Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Role '{user['role']}' is not authorized for this action",
            )
        return user
    return role_checker
