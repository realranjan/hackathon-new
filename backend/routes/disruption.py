import os
import json
import threading
from fastapi import APIRouter, Request, Body, HTTPException, Depends, Query
from models import DisruptionEvent, AlertResponse, GenAIPlanRequest, GenAIPlanResponse
from auth import get_current_user_role
from agents.risk_analyzer import analyze_risk
from agents.response_planner import generate_action_plan
from typing import Any, Dict, List
import logging
import datetime
from supabase import create_client
from dotenv import load_dotenv
from agents.event_monitor import fetch_air_events, fetch_sea_events, fetch_road_events
import asyncio

load_dotenv(dotenv_path=os.path.join("backend", ".env"))
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

disruption_router = APIRouter()

def log_api(event, **kwargs):
    ts = datetime.datetime.now().isoformat()
    print(f"[API] {ts} | {event} | " + " | ".join(f"{k}={v}" for k, v in kwargs.items()))

def log_agent(event, **kwargs):
    ts = datetime.datetime.now().isoformat()
    print(f"[AGENT] {ts} | {event} | " + " | ".join(f"{k}={v}" for k, v in kwargs.items()))

@disruption_router.post("/simulate_disruptions/", response_model=AlertResponse)
async def simulate_disruptions(request: Request, disruptions: List[DisruptionEvent] = Body(...), user=Depends(get_current_user_role("admin"))):
    log_api("simulate_disruptions_called", endpoint="/simulate_disruptions", disruptions=disruptions)
    alerts = []
    try:
        disruption_dicts = [event.dict() for event in disruptions]
        try:
            log_api("calling_analyze_risk")
            risk_report = analyze_risk(disruption_dicts)
            log_api("risk_report_generated", risk_report=risk_report)
        except RuntimeError as e:
            log_api("llm_risk_analysis_failed", error=str(e))
            logging.error(f"LLM risk analysis failed: {e}")
            raise HTTPException(status_code=500, detail=f"LLM-based risk analysis is required: {e}")
        try:
            log_api("calling_generate_action_plan")
            action_plan = generate_action_plan(risk_report)
            log_api("action_plan_generated", action_plan=action_plan)
        except Exception as e:
            log_api("action_plan_generation_failed", error=str(e))
            logging.error(f"Action plan generation failed: {e}")
            action_plan = []
        for event in disruptions:
            event_payload = event.dict()
            event_risks = risk_report
            event_plans = action_plan
            alert = {
                "event": event_payload,
                "risk_report": event_risks,
                "action_plan": event_plans
            }
            log_api("appending_alert", alert=alert)
            # Insert alert into Supabase
            supabase.table("alerts").insert(alert).execute()
            alerts.append(alert)
        log_api("returning_alerts_response", alerts=alerts)
        return {"alerts": alerts}
    except HTTPException:
        raise
    except Exception as e:
        log_api("simulation_failed", error=str(e))
        raise HTTPException(status_code=500, detail=f"Simulation failed: {e}")

@disruption_router.post("/genai_plan/", response_model=GenAIPlanResponse)
async def genai_plan_endpoint(request: Request, risk_report: List[Dict[str, Any]] = Body(...), user=Depends(get_current_user_role())):
    print("[API] /genai_plan/ called")
    try:
        print(f"[API] Received risk_report: {risk_report}")
        print("[API] Calling generate_action_plan...")
        action_plan = generate_action_plan(risk_report)
        print(f"[API] Action plan generated: {action_plan}")
    except Exception as e:
        print(f"[API] Action plan generation failed: {e}")
        logging.error(f"Action plan generation failed: {e}")
        action_plan = []
    print("[API] Returning action_plan response.")
    return {"action_plan": action_plan}

@disruption_router.get("/alerts/")
async def get_alerts():
    alerts = supabase.table("alerts").select("*").order("id", desc=True).execute().data or []
    # Ensure all required fields are present
    def enrich(alert):
        return {
            "id": alert.get("id", "unknown"),
            "isReal": alert.get("isReal", False),
            "severity": alert.get("severity", "medium"),
            "riskScore": alert.get("riskScore", 5),
            "affectedShipments": alert.get("affectedShipments", 0),
            "title": alert.get("title", "Alert"),
            "description": alert.get("description", "No description."),
            "location": alert.get("location", "Unknown"),
            "timeAgo": alert.get("timeAgo", "just now"),
            "type": alert.get("type", "General"),
            # Add any other fields as needed
            **alert
        }
    return {"alerts": [enrich(a) for a in alerts]}

@disruption_router.post("/chat/")
async def chat_endpoint(
    query: str = Body(..., embed=True),
    model: str = Query(None),
    user=Depends(get_current_user_role())
):
    try:
        log_api("chat_called", endpoint="/chat/", query=query, user=user["email"])
        # Use latest 10 alerts from Supabase as context
        context = supabase.table("alerts").select("*").order("id", desc=True).limit(10).execute().data or []
        prompt = f"You are a supply chain assistant. Here is recent alert data: {context}\nUser question: {query}\nAnswer in detail, using the data above."
        from langchain_groq import ChatGroq
        from langchain.prompts import PromptTemplate
        from langchain.chains import LLMChain
        import os
        model_name = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
        llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name=model_name)
        chain = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=["context", "query"], template="""{context}\nUser question: {query}\nAnswer in detail, using the data above."""))
        answer = chain.run(context=str(context), query=query)
        log_api("chat_answer", answer=answer, user=user["email"])
        # Log to audit_log
        supabase.table("audit_log").insert({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "actor": user["email"],
            "action": "llm_chat",
            "target": "chat",
            "details": f"Query: {query} | Model: {model_name}",
            "severity": "low",
            "status": "success",
            "ipAddress": "N/A",
            "userAgent": "N/A"
        }).execute()
        return {"answer": answer}
    except Exception as e:
        import logging
        logging.error(f"/chat/ endpoint failed: {e}")
        return {"error": str(e)}, 500

@disruption_router.get("/explain_risk/")
async def explain_risk(
    product_id: str = Query(...),
    model: str = Query(None),
    user=Depends(get_current_user_role())
):
    try:
        log_api("explain_risk_called", endpoint="/explain_risk/", product_id=product_id, user=user["email"])
        # Find the latest risk report for this product from Supabase alerts
        alerts = supabase.table("alerts").select("*").order("id", desc=True).execute().data or []
        for alert in alerts:
            for rr in alert.get("risk_report", []):
                if rr.get("product_id") == product_id:
                    # Use LLM to explain
                    from langchain_groq import ChatGroq
                    from langchain.prompts import PromptTemplate
                    from langchain.chains import LLMChain
                    import os
                    model_name = model or os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
                    llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name=model_name)
                    chain = LLMChain(llm=llm, prompt=PromptTemplate(input_variables=["risk"], template="""Explain in detail, for a supply chain manager, why this risk report was generated:\n{risk}"""))
                    explanation = chain.run(risk=str(rr))
                    log_api("explain_risk_explanation", explanation=explanation, risk_report=rr, user=user["email"])
                    # Log to audit_log
                    supabase.table("audit_log").insert({
                        "timestamp": datetime.datetime.utcnow().isoformat(),
                        "actor": user["email"],
                        "action": "llm_explain_risk",
                        "target": "explain_risk",
                        "details": f"Product: {product_id} | Model: {model_name}",
                        "severity": "low",
                        "status": "success",
                        "ipAddress": "N/A",
                        "userAgent": "N/A"
                    }).execute()
                    return {"explanation": explanation, "risk_report": rr}
        log_api("explain_risk_not_found", product_id=product_id, user=user["email"])
        return {"explanation": "No risk report found for this product_id.", "risk_report": None}
    except Exception as e:
        import logging
        logging.error(f"/explain_risk/ endpoint failed: {e}")
        return {"error": str(e)}, 500

@disruption_router.post("/batch_simulate_disruptions/")
async def batch_simulate_disruptions(disruptions: List[DisruptionEvent] = Body(...)):
    log_api("batch_simulate_disruptions_called", count=len(disruptions))
    disruption_dicts = [event.dict() for event in disruptions]
    risk_report = analyze_risk(disruption_dicts)
    action_plan = generate_action_plan(risk_report)
    log_api("batch_simulate_disruptions_result", risk_report=risk_report, action_plan=action_plan)
    # Insert a batch alert into Supabase for each disruption
    for event, rr, ap in zip(disruptions, risk_report, action_plan):
        alert = {
            "event": event.dict(),
            "risk_report": [rr],
            "action_plan": [ap] if isinstance(ap, dict) else ap
        }
        supabase.table("alerts").insert(alert).execute()
    return {"risk_report": risk_report, "action_plan": action_plan}

@disruption_router.post("/process_all_disruptions/")
async def process_all_disruptions(request: Request, simulated_disruptions: List[DisruptionEvent] = Body(default=[]), user=Depends(get_current_user_role("admin"))):
    log_api("process_all_disruptions_called", endpoint="/process_all_disruptions", simulated_disruptions=simulated_disruptions)
    alerts = []
    # Fetch real disruptions from agents
    real_events = []
    try:
        air_events, sea_events, road_events = await asyncio.gather(
            fetch_air_events(), fetch_sea_events(), fetch_road_events()
        )
        real_events = (air_events or []) + (sea_events or []) + (road_events or [])
    except Exception as e:
        log_api("real_agent_fetch_failed", error=str(e))
        real_events = []
    # Convert simulated disruptions to dicts
    simulated_dicts = [event.dict() for event in simulated_disruptions]
    # Combine all disruptions
    all_disruptions = real_events + simulated_dicts
    if not all_disruptions:
        return {"alerts": []}
    try:
        log_api("calling_analyze_risk")
        risk_report = analyze_risk(all_disruptions)
        log_api("risk_report_generated", risk_report=risk_report)
    except RuntimeError as e:
        log_api("llm_risk_analysis_failed", error=str(e))
        logging.error(f"LLM risk analysis failed: {e}")
        raise HTTPException(status_code=500, detail=f"LLM-based risk analysis is required: {e}")
    try:
        log_api("calling_generate_action_plan")
        action_plan = generate_action_plan(risk_report)
        log_api("action_plan_generated", action_plan=action_plan)
    except Exception as e:
        log_api("action_plan_generation_failed", error=str(e))
        logging.error(f"Action plan generation failed: {e}")
        action_plan = []
    # Store alerts
    for disruption in all_disruptions:
        alert = {
            "event": disruption,
            "risk_report": risk_report,
            "action_plan": action_plan
        }
        supabase.table("alerts").insert(alert).execute()
        alerts.append(alert)
    log_api("returning_alerts_response", alerts=alerts)
    return {"alerts": alerts}

@disruption_router.get("/risk_heatmap/")
async def risk_heatmap(user=Depends(get_current_user_role())):
    try:
        log_api("risk_heatmap_called", user=user["email"])
        # Aggregate risk scores by location from Supabase alerts
        alerts = supabase.table("alerts").select("*").execute().data or []
        location_risk = {}
        for alert in alerts:
            event = alert.get("event", {})
            loc = event.get("location")
            for rr in alert.get("risk_report", []):
                score = rr.get("risk_score", 0)
                if loc:
                    location_risk.setdefault(loc, []).append(score)
        # Compute average risk per location
        heatmap = [{"location": loc, "avg_risk": sum(scores)/len(scores) if scores else 0, "count": len(scores)} for loc, scores in location_risk.items()]
        log_api("risk_heatmap_result", heatmap=heatmap, user=user["email"])
        # Log to audit_log
        supabase.table("audit_log").insert({
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "actor": user["email"],
            "action": "llm_risk_heatmap",
            "target": "risk_heatmap",
            "details": "Heatmap generated",
            "severity": "low",
            "status": "success",
            "ipAddress": "N/A",
            "userAgent": "N/A"
        }).execute()
        return {"heatmap": heatmap}
    except Exception as e:
        import logging
        logging.error(f"/risk_heatmap/ endpoint failed: {e}")
        return {"error": str(e)}, 500