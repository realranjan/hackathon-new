from apscheduler.schedulers.background import BackgroundScheduler
from routes.disruption import alert_log, alert_lock
from agents.event_monitor import fetch_or_simulate_events
from agents.risk_analyzer import analyze_risk
from agents.response_planner import generate_action_plan
from utils.notifications import send_notification
import os
import json

def periodic_disruption_check():
    events = fetch_or_simulate_events()
    for event_payload in events:
        with alert_lock:
            if any(
                a["event"]["event_type"] == event_payload["event_type"] and
                a["event"]["location"] == event_payload["location"] and
                a["event"]["timestamp"] == event_payload["timestamp"]
                for a in alert_log
            ):
                continue
            risk_report = analyze_risk(event_payload)
            action_plan = generate_action_plan(risk_report)
            alert = {
                "event": event_payload,
                "risk_report": risk_report,
                "action_plan": action_plan
            }
            alert_log.append(alert)
            with open("alerts.json", "w") as f:
                json.dump(alert_log, f, indent=2)
            for rr in risk_report:
                if rr.get("escalation"):
                    subject = f"[SupplyWhiz] Escalation: {rr['product_id']} at {rr.get('current_location', rr.get('shipping_origin', '?'))}"
                    body = f"Escalation: {rr['escalation']}\nProduct: {rr['product_id']}\nLocation: {rr.get('current_location', rr.get('shipping_origin', '?'))}\nStatus: {rr.get('status', '?')}\nDetails: {rr}"
                    send_notification(
                        subject,
                        body,
                        channels=os.getenv("NOTIFY_CHANNELS", "email,slack").split(","),
                        to_email=os.getenv("NOTIFY_EMAIL"),
                        slack_channel=os.getenv("SLACK_CHANNEL"),
                        to_number=os.getenv("NOTIFY_PHONE")
                    )

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(periodic_disruption_check, 'interval', minutes=10)
    scheduler.start() 