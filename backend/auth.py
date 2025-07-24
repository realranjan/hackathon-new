from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db import get_mysql_pool, pwd_context, JWT_SECRET
from models import UserRegisterRequest, UserRegisterResponse, UserLoginRequest, UserLoginResponse
import jwt
from datetime import datetime, timedelta
import aiomysql
import warnings

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
        if not payload.get("is_active", True) or not payload.get("is_verified", False):
            raise HTTPException(status_code=403, detail="User not active or not verified")
        if required_role and payload["role"] != required_role and not payload["is_superuser"]:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return payload
    return dependency

@auth_router.post("/auth/register", response_model=UserRegisterResponse)
async def register_user(user: UserRegisterRequest):
    email = user.email.lower()
    password = user.password
    role = user.role
    is_active = user.is_active
    is_superuser = user.is_superuser
    is_verified = user.is_verified
    hashed_password = pwd_context.hash(password)
    pool = await get_mysql_pool()
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
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
            try:
                await cur.execute(
                    "INSERT INTO user (email, hashed_password, role, is_active, is_superuser, is_verified) VALUES (%s, %s, %s, %s, %s, %s)",
                    (email, hashed_password, role, is_active, is_superuser, is_verified)
                )
                await conn.commit()
                await cur.execute("SELECT * FROM user WHERE email=%s", (email,))
                db_user = await cur.fetchone()
            except aiomysql.IntegrityError:
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
    payload = {
        "sub": db_user["email"],
        "id": db_user["id"],
        "role": db_user["role"],
        "is_superuser": db_user["is_superuser"],
        "is_active": db_user["is_active"],
        "is_verified": db_user["is_verified"],
        "exp": datetime.utcnow() + timedelta(hours=1)
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