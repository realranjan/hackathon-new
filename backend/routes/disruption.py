from fastapi import APIRouter, Request, Body, HTTPException, Depends
from models import DisruptionEvent, AlertResponse, GenAIPlanRequest, GenAIPlanResponse
from auth import get_current_user_role
from agents.risk_analyzer import analyze_risk
from agents.response_planner import generate_action_plan
import os
import json
import threading
from typing import Any, Dict, List

ALERTS_FILE = "alerts.json"
if os.path.exists(ALERTS_FILE):
    with open(ALERTS_FILE, "r") as f:
        alert_log: List[dict] = json.load(f)
else:
    alert_log: List[dict] = []
alert_lock = threading.Lock()

disruption_router = APIRouter()

@disruption_router.post("/simulate_disruptions/", response_model=AlertResponse)
async def simulate_disruptions(request: Request, disruptions: List[DisruptionEvent] = Body(...), user=Depends(get_current_user_role("admin"))):
    alerts = []
    try:
        # Pass all disruptions at once to analyze_risk
        disruption_dicts = [event.dict() for event in disruptions]
        risk_report = analyze_risk(disruption_dicts)
        action_plan = generate_action_plan(risk_report)
        for event in disruptions:
            event_payload = event.dict()
            # Find all risk reports for this event (by location/event_type/timestamp)
            event_risks = [r for r in risk_report if r.get("disruption", {}).get("location") == event_payload["location"] and r.get("disruption", {}).get("event_type") == event_payload["event_type"] and r.get("disruption", {}).get("timestamp") == event_payload["timestamp"]]
            # Find all action plans for this event (by product_id or disruption)
            event_plans = [p for p in action_plan if any(r.get("product_id") == p.get("product_id") for r in event_risks)]
            alert = {
                "event": event_payload,
                "risk_report": event_risks,
                "action_plan": event_plans
            }
            with alert_lock:
                alert_log.append(alert)
                with open(ALERTS_FILE, "w") as f:
                    json.dump(alert_log, f, indent=2)
            alerts.append(alert)
        return {"alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {e}")

@disruption_router.post("/genai_plan/", response_model=GenAIPlanResponse)
async def genai_plan_endpoint(request: Request, risk_report: List[Dict[str, Any]] = Body(...), user=Depends(get_current_user_role())):
    action_plan = generate_action_plan(risk_report)
    return {"action_plan": action_plan}

@disruption_router.get("/alerts/", response_model=AlertResponse)
async def get_alerts():
    return {"alerts": alert_log} 