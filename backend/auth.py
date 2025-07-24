from fastapi import APIRouter, Depends, HTTPException, Body, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db import get_mysql_pool, pwd_context, JWT_SECRET
from models import UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse
import jwt
from datetime import datetime, timedelta
import aiomysql
import warnings
from pydantic import BaseModel, EmailStr, constr
import secrets
from audit import log_audit

auth_router = APIRouter()
security = HTTPBearer()

try:
    import bcrypt
    if not hasattr(bcrypt, "__about__") or not hasattr(bcrypt.__about__, "__version__"):
        warnings.warn("bcrypt version attribute missing; consider upgrading bcrypt and passlib.")
except ImportError:
    warnings.warn("bcrypt not installed; password hashing will fail.")

def get_current_user_role(required_role=None):
    async def dependency(credentials: HTTPAuthorizationCredentials = Depends(security)):
        try:
            payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
        except jwt.PyJWTError:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    return dependency

class PasswordChangeRequest(BaseModel):
    old_password: constr(min_length=6)
    new_password: constr(min_length=6)

@auth_router.post("/auth/register", response_model=UserRegisterResponse)
async def register_user(user: UserRegisterRequest, request: Request):
    actor = None
    auth_header = request.headers.get("authorization")
    if auth_header:
        try:
            token = auth_header.split(" ")[1]
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            actor = payload
        except Exception:
            pass
    pool = await get_mysql_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            # Always create the table if it doesn't exist
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS user (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    hashed_password VARCHAR(255) NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    is_superuser BOOLEAN DEFAULT FALSE,
                    is_verified BOOLEAN DEFAULT FALSE,
                    role VARCHAR(32) DEFAULT 'viewer'
                ) ENGINE=InnoDB;
            """)
            # Now you can safely query the table
            if user.role in ("admin", "operator"):
                await cur.execute("SELECT COUNT(*) as count FROM user WHERE role='admin'")
                count = (await cur.fetchone())["count"]
                if count > 0 and (not actor or actor["role"] != "admin"):
                    pool.close()
                    await pool.wait_closed()
                    raise HTTPException(status_code=403, detail="Only admin can register admin/operator users.")
            # Validate email and password
            if not user.email or not user.password or len(user.password) < 6:
                pool.close()
                await pool.wait_closed()
                raise HTTPException(status_code=400, detail="Invalid email or password (min 6 chars).")
            email = user.email.lower()
            password = user.password
            role = user.role
            is_active = user.is_active
            is_superuser = user.is_superuser
            is_verified = user.is_verified
            hashed_password = pwd_context.hash(password)
            try:
                await cur.execute(
                    "INSERT INTO user (email, hashed_password, role, is_active, is_superuser, is_verified) VALUES (%s, %s, %s, %s, %s, %s)",
                    (email, hashed_password, role, is_active, is_superuser, is_verified)
                )
                await conn.commit()
                await cur.execute("SELECT * FROM user WHERE email=%s", (email,))
                db_user = await cur.fetchone()
            except aiomysql.IntegrityError:
                pool.close()
                await pool.wait_closed()
                return {"message": "User already exists"}
    pool.close()
    await pool.wait_closed()
    return {
        "message": "User registered",
        "id": db_user["id"],
        "email": db_user["email"],
        "role": db_user["role"],
        "is_active": db_user["is_active"],
        "is_superuser": db_user["is_superuser"],
        "is_verified": db_user["is_verified"]
    }

@auth_router.post("/auth/login", response_model=UserLoginResponse)
async def login_user(user: UserLoginRequest):
    email = user.email.lower()
    password = user.password
    pool = await get_mysql_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM user WHERE email=%s", (email,))
            db_user = await cur.fetchone()
    pool.close()
    await pool.wait_closed()
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

@auth_router.post("/auth/change_password")
async def change_password(req: PasswordChangeRequest, actor=Depends(get_current_user_role())):
    email = actor["email"]
    pool = await get_mysql_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM user WHERE email=%s", (email,))
            db_user = await cur.fetchone()
            if not db_user or not pwd_context.verify(req.old_password, db_user["hashed_password"]):
                raise HTTPException(status_code=401, detail="Old password incorrect.")
            new_hashed = pwd_context.hash(req.new_password)
            await cur.execute("UPDATE user SET hashed_password=%s WHERE email=%s", (new_hashed, email))
            await conn.commit()
    pool.close()
    await pool.wait_closed()
    return {"message": "Password changed successfully."} 