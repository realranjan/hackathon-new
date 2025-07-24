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

@admin_router.get("/admin/audit_log/")
async def get_audit_log(user=Depends(get_current_user_role("admin"))):
    print("[API] /admin/audit_log/ called")
    logs = supabase.table("audit_log").select("*").order("timestamp", desc=True).limit(100).execute().data or []
    return {"logs": logs} 