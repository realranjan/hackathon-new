import os
import asyncio
from apscheduler.schedulers.background import BackgroundScheduler
from agents.event_monitor import fetch_or_simulate_events
from agents.risk_analyzer import analyze_risk
from agents.response_planner import generate_action_plan
from utils.notifications import send_notification
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join("backend", ".env"))
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def periodic_disruption_check():
    try:
        events = asyncio.run(fetch_or_simulate_events())
        for event_payload in events:
            # Check for duplicate event in Supabase
            existing = supabase.table("alerts").select("*").eq("event->>event_type", event_payload["event_type"]).eq("event->>location", event_payload["location"]).eq("event->>timestamp", event_payload["timestamp"]).execute().data
            if existing:
                continue
            risk_report = analyze_risk(event_payload)
            action_plan = generate_action_plan(risk_report)
            alert = {
                # Required fields for 'alerts' table
                "isreal": True,
                "severity": event_payload.get("severity", "medium"),
                "riskscore": risk_report["risk_score"] if isinstance(risk_report, dict) and "risk_score" in risk_report else 0,
                "affectedshipments": risk_report["affected_shipments"] if isinstance(risk_report, dict) and "affected_shipments" in risk_report else 0,
                "title": event_payload.get("event_type", "Disruption Alert"),
                "description": event_payload.get("description", "Disruption detected"),
                "location": event_payload.get("location", "Unknown"),
                "timeago": "just now",
                "type": event_payload.get("event_type", "disruption"),
                "event": event_payload,
                "risk_report": risk_report,
                "action_plan": action_plan
            }
            supabase.table("alerts").insert(alert).execute()
            # Optionally send notifications
            # send_notification(alert)
    except Exception as e:
        import logging
        logging.error(f"Scheduler disruption check failed: {e}")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_disruption_check, 'interval', minutes=10)
    scheduler.start() 