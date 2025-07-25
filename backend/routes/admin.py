from fastapi import APIRouter, Depends, HTTPException, Body, Query
from audit import log_audit
from db import get_all_users, create_user
import os
import json
from typing import Optional
from auth import get_current_user_role
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join("backend", ".env"))
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

admin_router = APIRouter()

@admin_router.get("/admin/users/")
async def list_users(user=Depends(get_current_user_role("admin")), page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100), search: str = Query(None)):
    print("[API] /admin/users/ called")
    users = get_all_users()
    if search:
        users = [u for u in users if search.lower() in u["email"].lower()]
    total = len(users)
    start = (page - 1) * page_size
    end = start + page_size
    return {"users": users[start:end], "total": total, "page": page, "page_size": page_size}

# TODO: Refactor update_user and delete_user to use Supabase

@admin_router.post("/admin/users/")
async def create_user_endpoint(user_data: dict = Body(...), user=Depends(get_current_user_role("admin"))):
    """Create a new user (admin only)."""
    # Validate required fields
    required_fields = ["email", "password", "role"]
    for field in required_fields:
        if field not in user_data:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    # Hash password
    from db import pwd_context
    user_data["hashed_password"] = pwd_context.hash(user_data.pop("password"))
    user_data["is_active"] = user_data.get("is_active", True)
    user_data["is_superuser"] = user_data.get("is_superuser", False)
    user_data["is_verified"] = user_data.get("is_verified", False)
    # Insert into Supabase
    result = supabase.table("user").insert(user_data).execute().data
    return {"user": result}

@admin_router.put("/admin/users/{user_id}")
async def update_user_endpoint(user_id: str, update_data: dict = Body(...), user=Depends(get_current_user_role("admin"))):
    """Update an existing user (admin only)."""
    try:
        if "password" in update_data:
            from db import pwd_context
            update_data["hashed_password"] = pwd_context.hash(update_data.pop("password"))
        result = supabase.table("user").update(update_data).eq("id", user_id).execute().data
        if not result:
            raise HTTPException(status_code=404, detail="User not found or update failed")
        return {"user": result}
    except Exception as e:
        import logging
        logging.error(f"/admin/users/{{user_id}} PUT endpoint failed: {e}")
        return {"error": str(e)}, 500

@admin_router.delete("/admin/users/{user_id}")
async def delete_user_endpoint(user_id: str, user=Depends(get_current_user_role("admin"))):
    """Delete a user (admin only)."""
    result = supabase.table("user").delete().eq("id", user_id).execute().data
    if not result:
        raise HTTPException(status_code=404, detail="User not found or delete failed")
    return {"deleted": True, "user_id": user_id}

@admin_router.get("/admin/audit_log/")
async def get_audit_log(user=Depends(get_current_user_role("admin"))):
    logs = supabase.table("audit_log").select("*").order("timestamp", desc=True).limit(100).execute().data or []
    return {"logs": logs} 