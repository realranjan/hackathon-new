import streamlit as st
import requests
import pandas as pd
import time
import json
import plotly.express as px
import plotly.graph_objects as go

st.title("SupplyWhiz Dashboard")

# Simple geocoding for demo locations
LOCATION_COORDS = {
    "Bangalore Port": {"lat": 12.95, "lon": 77.7},
    "Bangalore": {"lat": 12.97, "lon": 77.59},
    "Chennai": {"lat": 13.08, "lon": 80.27},
    "Mumbai": {"lat": 19.07, "lon": 72.88},
}

if st.button("Simulate Disruption: Strike at Bangalore Port"):
    event = {
        "location": "Bangalore Port",
        "event_type": "Strike",
        "severity": "High",
        "timestamp": "2024-06-01T12:00:00Z",
        "source": "Simulated"
    }
    response = requests.post("http://localhost:8000/simulate_event/", json=event)
    st.success("Disruption simulated!")

st.header("Real-Time Alerts")
# Throttle alert fetching to once every 10 seconds
if 'last_alert_fetch' not in st.session_state:
    st.session_state['last_alert_fetch'] = 0
now = time.time()
if now - st.session_state['last_alert_fetch'] > 10:
    alerts = requests.get("http://localhost:8000/alerts/").json().get("alerts", [])
    st.session_state['alerts'] = alerts
    st.session_state['last_alert_fetch'] = now
else:
    alerts = st.session_state.get('alerts', [])

if not alerts:
    st.write("No alerts yet.")
else:
    for i, alert in enumerate(reversed(alerts), 1):
        st.subheader(f"Alert #{len(alerts)-i+1}")
        st.markdown("**Event:**")
        st.json(alert["event"])
        st.markdown("**Risk Report:**")
        st.json(alert["risk_report"])
        st.markdown("**Action Plan:**")
        st.json(alert["action_plan"])
        st.markdown(f"**Risk Score:** {alert['action_plan'].get('risk_score', 'N/A')}")
        st.markdown("---")

# Map overlay for disruption locations
st.header("Disruption Map")
map_data = []
for alert in alerts:
    loc = alert["event"].get("location")
    coords = LOCATION_COORDS.get(loc)
    if coords:
        map_data.append({"lat": coords["lat"], "lon": coords["lon"]})
if map_data:
    st.map(pd.DataFrame(map_data))
else:
    st.write("No disruption locations to display on map.")

# Analytics section
st.header("📊 Alert Analytics")
if alerts:
    # Total alerts
    st.metric("Total Alerts", len(alerts))
    # Average risk score
    risk_scores = [a["action_plan"].get("risk_score", 0) for a in alerts if a["action_plan"].get("risk_score") is not None]
    if risk_scores:
        st.metric("Average Risk Score", round(sum(risk_scores)/len(risk_scores), 2))
    # Bar chart of alert counts by event type
    event_types = [a["event"].get("event_type", "Unknown") for a in alerts]
    event_type_counts = pd.Series(event_types).value_counts()
    st.bar_chart(event_type_counts)
else:
    st.write("No analytics to display yet.")

# --- Real-Time Shipment Update Form ---
st.header("Update Shipment Location/Status")
try:
    inventory = requests.get("http://localhost:8000/alerts/").json().get("alerts", [])
    # Extract unique product_ids from risk reports for selection
    all_shipments = set()
    for alert in inventory:
        for rr in alert.get("risk_report", []):
            all_shipments.add(rr.get("product_id"))
    all_shipments = sorted(list(all_shipments))
except Exception:
    all_shipments = []

if all_shipments:
    product_id = st.selectbox("Select Shipment", all_shipments)
    new_location = st.text_input("New Current Location")
    new_status = st.selectbox("Status", ["in_transit", "rerouted", "delayed", "delivered"])
    if st.button("Update Shipment"):
        update = {"product_id": product_id, "current_location": new_location, "status": new_status}
        response = requests.post("http://localhost:8000/update_shipment/", json=update)
        st.write(response.json())
else:
    st.info("No shipments available to update yet.")

# --- Multi-Disruption Simulation ---
st.header("Simulate Multiple Disruptions")
def example_disruptions():
    return '[\n  {"location": "Hubli", "event_type": "Flood", "severity": "High", "timestamp": "2024-06-10T10:00:00Z", "source": "Simulated", "mode": "road"},\n  {"location": "Nagpur", "event_type": "Strike", "severity": "Medium", "timestamp": "2024-06-11T12:00:00Z", "source": "Simulated", "mode": "road"}\n]'

disruptions_json = st.text_area("Paste disruptions as JSON array", value=example_disruptions(), height=150)
if st.button("Simulate Disruptions"):
    try:
        disruptions = json.loads(disruptions_json)
        response = requests.post("http://localhost:8000/simulate_disruptions/", json=disruptions)
        st.json(response.json())
    except Exception as e:
        st.error(f"Invalid JSON or API error: {e}")

# --- Show Current Shipments and Status ---
st.header("Current Shipments")
try:
    with open("../data/inventory.json") as f:
        inv = json.load(f)
    for item in inv:
        st.markdown(f"**Product:** {item['product_id']} | **From:** {item['shipping_origin']} | **To:** {item['destination']} | **Current:** {item.get('current_location', 'Unknown')} | **Status:** {item.get('status', 'Unknown')}")
        st.markdown(f"Route: {' → '.join(item.get('route', []))}")
        st.markdown(f"Legs: {item.get('legs', [])}")
        st.markdown("---")
except Exception as e:
    st.info(f"Could not load inventory: {e}")

# --- Scenario: Move shipment and simulate disruption at new location ---
st.header("Demo Scenario: Move Shipment and Simulate Disruption")
if all_shipments:
    scenario_product = st.selectbox("Select Shipment for Scenario", all_shipments, key="scenario_select")
    new_scenario_location = st.text_input("Scenario: New Location", value="Pune", key="scenario_loc")
    if st.button("Run Scenario: Move and Disrupt"):
        # 1. Update shipment location
        update = {"product_id": scenario_product, "current_location": new_scenario_location, "status": "in_transit"}
        update_resp = requests.post("http://localhost:8000/update_shipment/", json=update)
        st.write("Shipment updated:", update_resp.json())
        # 2. Simulate disruption at new location
        disruption = [{
            "location": new_scenario_location,
            "event_type": "Flood",
            "severity": "High",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": "Simulated",
            "mode": "road"
        }]
        sim_resp = requests.post("http://localhost:8000/simulate_disruptions/", json=disruption)
        st.write("Disruption simulated:", sim_resp.json())

# --- Escalation Dashboard ---
st.header("🚨 Escalation Dashboard")
escalated = []
for alert in alerts:
    for rr in alert.get("risk_report", []):
        if rr.get("escalation"):
            escalated.append({"product_id": rr["product_id"], "escalation": rr["escalation"], "location": rr.get("current_location", rr.get("shipping_origin", "?")), "status": rr.get("status", "?")})
if escalated:
    for esc in escalated:
        st.error(f"Product: {esc['product_id']} | Location: {esc['location']} | Status: {esc['status']} | Escalation: {esc['escalation']}")
else:
    st.success("No escalated shipments at this time.")

# --- Timeline View for Each Shipment ---
st.header("Shipment Timelines")
try:
    with open("../data/inventory.json") as f:
        inv = json.load(f)
    for item in inv:
        st.markdown(f"### Product: {item['product_id']} | Status: {item.get('status', 'Unknown')}")
        if "legs" in item and item["legs"]:
            for i, leg in enumerate(item["legs"]):
                st.markdown(f"Leg {i+1}: {leg['origin']} → {leg['destination']} | Current: {leg.get('current_location', '?')} | Status: {leg.get('status', '?')} | ETA: {leg.get('eta', '?')}")
        else:
            st.markdown("No legs data available.")
        st.markdown("---")
except Exception as e:
    st.info(f"Could not load inventory for timeline: {e}")

# --- Animated Map with Plotly ---
st.header("Animated Shipment Map (Demo)")
try:
    with open("../data/inventory.json") as f:
        inv = json.load(f)
    # Build a DataFrame for all legs and current locations
    map_rows = []
    for item in inv:
        color = "red" if item.get("status") == "delayed" else ("orange" if item.get("status") == "rerouted" else "blue")
        for leg in item.get("legs", []):
            loc = leg.get("current_location") or leg.get("destination")
            if loc and loc in LOCATION_COORDS:
                coords = LOCATION_COORDS[loc]
                map_rows.append({
                    "product_id": item["product_id"],
                    "location": loc,
                    "lat": coords["lat"],
                    "lon": coords["lon"],
                    "status": leg.get("status", "?"),
                    "color": color
                })
    if map_rows:
        df = pd.DataFrame(map_rows)
        fig = px.scatter_mapbox(
            df,
            lat="lat",
            lon="lon",
            color="product_id",
            hover_name="location",
            hover_data=["status"],
            zoom=4,
            height=400
        )
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_traces(marker=dict(size=14))
        st.plotly_chart(fig)
    else:
        st.info("No shipment locations to animate.")
except Exception as e:
    st.info(f"Could not load inventory for animated map: {e}")

# --- Timeline Chart for Each Shipment (Plotly) ---
st.header("Shipment Timelines (Plotly)")
try:
    with open("../data/inventory.json") as f:
        inv = json.load(f)
    for item in inv:
        if "legs" in item and item["legs"]:
            fig = go.Figure()
            for i, leg in enumerate(item["legs"]):
                fig.add_trace(go.Scatter(
                    x=[leg["origin"], leg["destination"]],
                    y=[i, i],
                    mode="lines+markers+text",
                    text=[leg["status"], leg["status"]],
                    marker=dict(size=12, color="green" if leg["status"]=="completed" else ("orange" if leg["status"]=="in_transit" else "red")),
                    line=dict(width=4),
                    name=f"Leg {i+1}"
                ))
            fig.update_layout(title=f"Product {item['product_id']} Timeline", xaxis_title="Location", yaxis_title="Leg #", showlegend=False)
            st.plotly_chart(fig)
        else:
            st.markdown(f"No legs data for {item['product_id']}.")
except Exception as e:
    st.info(f"Could not load inventory for timeline chart: {e}") 