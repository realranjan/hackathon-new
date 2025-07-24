from fastapi import APIRouter, Depends, HTTPException, Body, Query
from audit import log_audit
from db import get_mysql_pool
import aiomysql
import os
import json
from typing import Optional
# Move this import after all other imports to avoid circular import issues
from auth import get_current_user_role

admin_router = APIRouter()
AUDIT_LOG_FILE = "audit_log.json"

@admin_router.get("/admin/users/")
async def list_users(
    user=Depends(get_current_user_role("admin")),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: str = Query(None)
):
    print("[API] /admin/users/ called")
    pool = await get_mysql_pool()
    offset = (page - 1) * page_size
    base_query = "SELECT id, email, role, is_active, is_superuser, is_verified FROM user"
    params = []
    if search:
        base_query += " WHERE email LIKE %s"
        params.append(f"%{search}%")
    base_query += " ORDER BY id LIMIT %s OFFSET %s"
    params.extend([page_size, offset])
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute(base_query, tuple(params))
            users = await cur.fetchall()
            # Get total count
            if search:
                await cur.execute("SELECT COUNT(*) as count FROM user WHERE email LIKE %s", (f"%{search}%",))
            else:
                await cur.execute("SELECT COUNT(*) as count FROM user")
            total = (await cur.fetchone())["count"]
    pool.close()
    await pool.wait_closed()
    return {"users": users, "total": total, "page": page, "page_size": page_size}

@admin_router.post("/admin/user/update/")
async def update_user(user_id: int = Body(...), role: Optional[str] = Body(None), is_active: Optional[bool] = Body(None), is_verified: Optional[bool] = Body(None), actor=Depends(get_current_user_role("admin"))):
    print(f"[API] /admin/user/update/ called for user_id={user_id}")
    pool = await get_mysql_pool()
    updates = []
    params = []
    if role:
        updates.append("role=%s")
        params.append(role)
    if is_active is not None:
        updates.append("is_active=%s")
        params.append(is_active)
    if is_verified is not None:
        updates.append("is_verified=%s")
        params.append(is_verified)
    if not updates:
        raise HTTPException(status_code=400, detail="No fields to update.")
    params.append(user_id)
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM user WHERE id=%s", (user_id,))
            user_row = await cur.fetchone()
            if not user_row:
                pool.close()
                await pool.wait_closed()
                raise HTTPException(status_code=404, detail="User not found.")
            await cur.execute(f"UPDATE user SET {', '.join(updates)} WHERE id=%s", tuple(params))
            await conn.commit()
    pool.close()
    await pool.wait_closed()
    log_audit("update_user", actor["email"], target=user_id, details={"role": role, "is_active": is_active, "is_verified": is_verified})
    return {"message": "User updated"}

@admin_router.post("/admin/user/delete/")
async def delete_user(user_id: int = Body(...), actor=Depends(get_current_user_role("admin"))):
    print(f"[API] /admin/user/delete/ called for user_id={user_id}")
    pool = await get_mysql_pool()
    # Prevent deleting the last admin
    async with pool.acquire() as conn:
        async with conn.cursor(aiomysql.DictCursor) as cur:
            await cur.execute("SELECT * FROM user WHERE id=%s", (user_id,))
            user_row = await cur.fetchone()
            if not user_row:
                pool.close()
                await pool.wait_closed()
                raise HTTPException(status_code=404, detail="User not found.")
            if user_row["role"] == "admin":
                await cur.execute("SELECT COUNT(*) as count FROM user WHERE role='admin'")
                count = (await cur.fetchone())["count"]
                if count <= 1:
                    pool.close()
                    await pool.wait_closed()
                    raise HTTPException(status_code=400, detail="Cannot delete the last admin user.")
            if user_row["email"] == actor["email"]:
                pool.close()
                await pool.wait_closed()
                raise HTTPException(status_code=400, detail="You cannot delete your own user account.")
            await cur.execute("DELETE FROM user WHERE id=%s", (user_id,))
            await conn.commit()
    pool.close()
    await pool.wait_closed()
    log_audit("delete_user", actor["email"], target=user_id)
    return {"message": "User deleted"}

@admin_router.get("/admin/audit_log/")
async def get_audit_log(user=Depends(get_current_user_role("admin"))):
    print("[API] /admin/audit_log/ called")
    if os.path.exists(AUDIT_LOG_FILE):
        with open(AUDIT_LOG_FILE, "r") as f:
            log = json.load(f)
    else:
        log = []
    return {"logs": log} 