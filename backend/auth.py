from fastapi import APIRouter, Depends, HTTPException, Body, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db import pwd_context, JWT_SECRET, get_user_by_email, create_user
from models import UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse
import jwt
from datetime import datetime, timedelta
import warnings
from pydantic import BaseModel, EmailStr, constr
import secrets
from audit import log_audit

auth_router = APIRouter()
security = HTTPBearer()

# TEMPORARY: Disable authentication for all endpoints during development
# Restore real auth before production!
def get_current_user_role(required_role=None):
    def dependency(request=None):
        # Return a dummy user with admin role for all requests
        return {
            "email": "dev@local.test",
            "id": 1,
            "role": "admin",
            "is_superuser": True,
            "is_active": True,
            "is_verified": True
        }
    return dependency

class PasswordChangeRequest(BaseModel):
    old_password: constr(min_length=6)
    new_password: constr(min_length=6)

@auth_router.post("/auth/register", response_model=UserRegisterResponse)
async def register_user(user: UserRegisterRequest):
    email = user.email.lower()
    password = user.password
    hashed_password = pwd_context.hash(password)
    user_dict = {"email": email, "hashed_password": hashed_password, "role": user.role, "is_active": True, "is_superuser": False, "is_verified": False}
    create_user(user_dict)
    return {"message": "User registered"}

@auth_router.post("/auth/login", response_model=UserLoginResponse)
async def login_user(user: UserLoginRequest):
    email = user.email.lower()
    password = user.password
    db_user = get_user_by_email(email)
    if not db_user or not pwd_context.verify(password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    # Set token expiry: admin/superuser = 10 years, others = 1 hour
    if db_user["role"] == "admin" or db_user["is_superuser"]:
        exp = datetime.utcnow() + timedelta(days=3650)  # 10 years
    else:
        exp = datetime.utcnow() + timedelta(hours=1)
    payload = {
        "sub": db_user["email"],
        "id": db_user["id"],
        "role": db_user["role"],
        "is_superuser": db_user["is_superuser"],
        "is_active": db_user["is_active"],
        "is_verified": db_user["is_verified"],
        "exp": exp
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    return {
        "access_token": token,
        "token_type": "bearer",
        "id": db_user["id"],
        "email": db_user["email"],
        "role": db_user["role"],
        "is_active": db_user["is_active"],
        "is_superuser": db_user["is_superuser"],
        "is_verified": db_user["is_verified"]
    }

# TODO: Refactor change_password to use Supabase
@auth_router.post("/auth/change_password")
async def change_password(req: PasswordChangeRequest, actor=Depends(get_current_user_role())):
    raise HTTPException(status_code=501, detail="Change password not implemented for Supabase yet.") 