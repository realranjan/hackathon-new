from fastapi import APIRouter, Body, WebSocket, WebSocketDisconnect, Query
from supabase import create_client
import os
import asyncio
import random
from datetime import datetime
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join("backend", ".env"))
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

analytics_router = APIRouter()

user_settings_store = {}

# --- Analytics Endpoints for Dashboard KPIs ---
@analytics_router.get("/analytics/risk_categories/")
async def get_risk_categories():
    try:
        resp = supabase.table("risk_categories").select("*").execute()
        return {"categories": resp.data or []}
    except Exception as e:
        import logging
        logging.error(f"/analytics/risk_categories/ endpoint failed: {e}")
        return {"error": str(e)}, 500

@analytics_router.get("/analytics/shipment_volume/")
async def get_shipment_volume():
    try:
        resp = supabase.table("shipment_volume").select("*").execute()
        return {"volume": resp.data or []}
    except Exception as e:
        import logging
        logging.error(f"/analytics/shipment_volume/ endpoint failed: {e}")
        return {"error": str(e)}, 500

@analytics_router.get("/analytics/on_time_delivery/")
async def get_on_time_delivery():
    resp = supabase.table("analytics_metrics").select("on_time_delivery").order("timestamp", desc=True).limit(1).execute()
    if resp.data and len(resp.data) > 0:
        return {"on_time_delivery": resp.data[0].get("on_time_delivery", 0)}
    return {"on_time_delivery": 0}

# --- Performance Metrics (extend as needed) ---
@analytics_router.get("/analytics/performance_metrics/")
async def get_performance_metrics(
    start: str = Query(None),
    end: str = Query(None),
    metric: str = Query(None)
):
    q = supabase.table("analytics_metrics").select("*")
    if start:
        q = q.gte("timestamp", start)
    if end:
        q = q.lte("timestamp", end)
    q = q.order("timestamp", desc=True)
    resp = q.execute()
    data = resp.data or []
    if metric:
        return {"metric": metric, "series": [{"timestamp": d["timestamp"], "value": d.get(metric)} for d in data if metric in d]}
    if start or end:
        return {"metrics": data}
    # Default: return latest as top-level fields
    if data:
        return data[0]
    return {}

# --- Workflow Steps (detailed for frontend) ---
@analytics_router.get("/workflow/steps/")
async def get_workflow_steps(workflow_id: str = Query(None)):
    q = supabase.table("workflow_steps").select("*").order("step_number")
    if workflow_id:
        q = q.eq("workflow_id", workflow_id)
    resp = q.execute()
    return {"steps": resp.data or []}

@analytics_router.get("/workflow/progress/")
async def get_workflow_progress():
    try:
        resp = supabase.table("workflow_steps").select("step_number").order("step_number", desc=True).limit(1).execute()
        total_steps = resp.data[0]["step_number"] if resp.data and len(resp.data) > 0 else 0
        # For demo, assume current step is 1
        return {"progress": {"step": 1, "total_steps": total_steps}}
    except Exception as e:
        import logging
        logging.error(f"/workflow/progress/ endpoint failed: {e}")
        return {"error": str(e)}, 500

# --- Tool Calls Panel (detailed tool call info) ---
@analytics_router.get("/tool_calls/")
async def get_tool_calls(page: int = 1, page_size: int = 20):
    start = (page - 1) * page_size
    resp = supabase.table("tool_calls").select("*").range(start, start + page_size - 1).order("timestamp", desc=True).execute()
    tool_calls = resp.data or []
    total = resp.count if hasattr(resp, 'count') and resp.count is not None else len(tool_calls)
    return {"tool_calls": tool_calls, "total": total, "page": page, "page_size": page_size}

# --- Agent Network Visualization (with node metadata) ---
@analytics_router.get("/agents/network/")
async def get_agents_network():
    resp = supabase.table("agents_network").select("*").execute()
    if resp.data and len(resp.data) > 0:
        nodes = [n for n in resp.data if n.get("type") == "node"]
        edges = [e for e in resp.data if n.get("type") == "edge"]
        return {"network": {"nodes": nodes, "edges": edges}}
    return {"network": {"nodes": [], "edges": []}}

# --- Global Port Status (with coordinates) ---
@analytics_router.get("/ports/status/")
async def get_ports_status(port_id: str = Query(None)):
    q = supabase.table("port_status").select("*")
    if port_id:
        q = q.eq("id", port_id)
    resp = q.execute()
    return {"ports": resp.data or []}

# --- User Settings (GET/POST for preferences) ---
@analytics_router.get("/user/settings/")
async def get_user_settings(user_id: str = "demo"):  # In real use, get from auth
    resp = supabase.table("user_settings").select("settings").eq("user_id", user_id).execute()
    if resp.data and len(resp.data) > 0 and resp.data[0].get("settings"):
        return {"settings": resp.data[0]["settings"]}
    # Default settings if not found
    return {"settings": {
        "notifications": {"email": True, "sms": False, "slack": True},
        "display": {"theme": "dark", "density": "comfortable"},
        "integrations": {"traccar": True, "project44": False}
    }}

@analytics_router.post("/user/settings/")
async def update_user_settings(settings: dict = Body(...), user_id: str = "demo"):  # In real use, get from auth
    # Upsert user settings
    supabase.table("user_settings").upsert({"user_id": user_id, "settings": settings}).execute()
    return {"settings": settings}

# --- Simulation State (for AI demo context) ---
@analytics_router.get("/simulation/state/")
async def get_simulation_state():
    resp = supabase.table("simulation_state").select("*").order("updated_at", desc=True).limit(1).execute()
    if resp.data and len(resp.data) > 0:
        return {"state": resp.data[0]}
    return {"state": {}}

@analytics_router.get("/agents/list/")
async def get_agents_list():
    resp = supabase.table("agents").select("*").execute()
    return {"agents": resp.data or []}

@analytics_router.post("/agents/update_status/")
async def update_agent_status(agent_id: str = Body(...), new_status: str = Body(...)):
    # Update agent status in Supabase
    resp = supabase.table("agents").update({"status": new_status}).eq("id", agent_id).execute()
    if not resp.data:
        return {"success": False, "error": "Agent not found or update failed."}
    return {"success": True, "agent_id": agent_id, "new_status": new_status}

@analytics_router.websocket("/ws/agents/")
async def websocket_agents(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            # Fetch all agents from DB
            agents = supabase.table("agents").select("*").execute().data or []
            if agents:
                # Simulate a random status update
                agent = random.choice(agents)
                agent["status"] = random.choice(["active", "idle", "offline"])
                await websocket.send_json({"type": "agent_update", "agent": agent})
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        pass 

@analytics_router.get("/check_integrations")
async def check_integrations():
    resp = supabase.table("integrations").select("*").execute()
    return {"integration_status": resp.data or []} 

@analytics_router.get("/analytics/risk_trends/")
async def get_risk_trends(start: str = Query(None), end: str = Query(None), risk_type: str = Query(None)):
    q = supabase.table("risk_trends").select("*")
    if start:
        q = q.gte("timestamp", start)
    if end:
        q = q.lte("timestamp", end)
    if risk_type:
        q = q.eq("type", risk_type)
    q = q.order("timestamp", desc=True)
    resp = q.execute()
    return {"riskData": resp.data or []}

@analytics_router.get("/analytics/port_performance/")
async def get_port_performance(start: str = Query(None), end: str = Query(None), port_id: str = Query(None)):
    q = supabase.table("port_performance").select("*")
    if start:
        q = q.gte("timestamp", start)
    if end:
        q = q.lte("timestamp", end)
    if port_id:
        q = q.eq("port_id", port_id)
    q = q.order("timestamp", desc=True)
    resp = q.execute()
    return {"ports": resp.data or []} 

@analytics_router.get("/analytics/kpis/")
async def get_kpis():
    # Aggregate KPIs for dashboard
    # Example: fetch from analytics_metrics, shipment, alerts, etc.
    # You may need to adjust queries based on your schema and data
    kpis = {}
    # Cost savings (latest)
    cost_savings = 0
    resp = supabase.table("analytics_metrics").select("cost_savings").order("timestamp", desc=True).limit(1).execute()
    if resp.data and len(resp.data) > 0:
        cost_savings = resp.data[0].get("cost_savings", 0)
    kpis["cost_savings"] = cost_savings
    # Active shipments
    resp = supabase.table("shipment").select("*", count="exact").eq("status", "in-transit").execute()
    kpis["active_shipments"] = resp.count if hasattr(resp, 'count') and resp.count is not None else len(resp.data or [])
    # Risk alerts (count)
    resp = supabase.table("alerts").select("*", count="exact").execute()
    kpis["risk_alerts"] = resp.count if hasattr(resp, 'count') and resp.count is not None else len(resp.data or [])
    # On-time delivery (latest)
    resp = supabase.table("analytics_metrics").select("on_time_delivery").order("timestamp", desc=True).limit(1).execute()
    if resp.data and len(resp.data) > 0:
        kpis["on_time_delivery"] = resp.data[0].get("on_time_delivery", 0)
    else:
        kpis["on_time_delivery"] = 0
    return kpis 