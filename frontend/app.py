import streamlit as st
import requests
import pandas as pd
import time
import json
import plotly.express as px
import plotly.graph_objects as go

st.title("SupplyWhiz Dashboard")

# --- Fetch shipments and locations from backend ---
API_BASE = "http://localhost:8000"
try:
    shipments = requests.get(f"{API_BASE}/shipments/").json().get("shipments", [])
    all_locations = set()
    all_shipments = set()
    for item in shipments:
        all_shipments.add(item.get("product_id"))
        all_locations.update(item.get("route", []))
        if item.get("current_location"):
            all_locations.add(item["current_location"])
        for leg in item.get("legs", []):
            if leg.get("origin"): all_locations.add(leg["origin"])
            if leg.get("destination"): all_locations.add(leg["destination"])
            if leg.get("current_location"): all_locations.add(leg["current_location"])
    all_locations = sorted(list(all_locations))
    all_shipments = sorted(list(all_shipments))
except Exception as e:
    all_locations = []
    all_shipments = []

# --- Authentication ---
def login(email, password):
    resp = requests.post(f"{API_BASE}/auth/login", json={"email": email, "password": password})
    if resp.status_code == 200:
        data = resp.json()
        st.session_state["jwt"] = data["access_token"]
        st.session_state["user"] = {
            "email": data["email"],
            "role": data["role"],
            "is_active": data["is_active"],
            "is_superuser": data["is_superuser"],
            "is_verified": data["is_verified"]
        }
        return True
    else:
        st.error(resp.json().get("detail", "Login failed"))
        return False

def register(email, password, role):
    resp = requests.post(f"{API_BASE}/auth/register", json={"email": email, "password": password, "role": role})
    if resp.status_code == 200 and resp.json().get("message") == "User registered":
        st.success("Registration successful! Please log in.")
        return True
    else:
        st.error(resp.json().get("message", "Registration failed"))
        return False

def api_request(method, endpoint, **kwargs):
    print(f"[FRONTEND] API request: {method} {endpoint} kwargs={kwargs}")
    headers = kwargs.pop("headers", {})
    if "jwt" in st.session_state:
        headers["Authorization"] = f"Bearer {st.session_state['jwt']}"
    try:
        resp = requests.request(method, f"{API_BASE}{endpoint}", headers=headers, **kwargs)
        print(f"[FRONTEND] API response: {resp.status_code} {resp.text}")
        return resp
    except Exception as e:
        print(f"[FRONTEND] API request error: {e}")
        raise

# --- Auth UI ---
if "jwt" not in st.session_state or "user" not in st.session_state:
    st.header("Login or Register")
    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login"):
            print(f"[FRONTEND] User attempting login: {email}")
            print(f"[FRONTEND] Login input: email={email}, password={'*' * len(password)}")
            if login(email, password):
                st.success("Login successful")
    with tab2:
        email = st.text_input("Email", key="reg_email")
        password = st.text_input("Password", type="password", key="reg_pass")
        role = st.selectbox("Role", ["admin", "operator", "viewer"], key="reg_role")
        if st.button("Register"):
            print(f"[FRONTEND] User attempting registration: {email}, role: {role}")
            print(f"[FRONTEND] Register input: email={email}, password={'*' * len(password)}, role={role}")
            register(email, password, role)
    st.stop()

user = st.session_state["user"]
st.success(f"Logged in as {user['email']} ({user['role']})")
if st.button("Logout"):
    st.session_state.clear()
    st.success("Logged out")

# --- Password Change UI ---
st.header("Change Password")
if st.button("Show Password Change Form"):
    with st.form("change_password_form"):
        old_password = st.text_input("Old Password", type="password", key="old_pass")
        new_password = st.text_input("New Password", type="password", key="new_pass")
        submit = st.form_submit_button("Change Password")
        if submit:
            resp = api_request("POST", "/auth/change_password", json={"old_password": old_password, "new_password": new_password})
            if resp.status_code == 200:
                st.success("Password changed successfully.")
            else:
                st.error(resp.json().get("detail", "Password change failed."))

# --- Role-based feature display ---
role = user["role"]
is_admin = role == "admin" or user.get("is_superuser")
is_operator = role == "operator" or is_admin
is_viewer = role == "viewer" or is_operator or is_admin

# --- Disruption Simulation UI ---
st.header("Simulate Disruption")
if all_locations:
    location = st.selectbox("Disruption Location", all_locations, key="disrupt_loc")
    event_type = st.selectbox("Event Type", ["Strike", "Flood", "Port Closure", "Protest", "Shutdown", "Instability", "Earthquake", "Hurricane"], key="disrupt_type")
    severity = st.selectbox("Severity", ["High", "Medium", "Low"], key="disrupt_severity")
    timestamp = st.text_input("Timestamp (YYYY-MM-DDTHH:MM:SSZ)", value=time.strftime("%Y-%m-%dT%H:%M:%SZ"), key="disrupt_time")
    source = st.text_input("Source", value="Simulated", key="disrupt_source")
    if st.button("Simulate Disruption", key="simulate_disrupt_btn"):
        print(f"[FRONTEND] Simulating disruption at {location} of type {event_type} with severity {severity}")
        print(f"[FRONTEND] Disruption input: location={location}, event_type={event_type}, severity={severity}, timestamp={timestamp}, source={source}")
        event = {
            "location": location,
            "event_type": event_type,
            "severity": severity,
            "timestamp": timestamp,
            "source": source
        }
        response = api_request("POST", "/simulate_disruptions/", json=[event])
        print(f"[FRONTEND] Simulate Disruption API response: {response.status_code} {response.text}")
        if response.status_code == 200:
            st.success("Disruption simulated!")
        else:
            st.error(response.json().get("detail", "Simulation failed."))
else:
    st.warning("No valid locations found in inventory for disruption simulation.")

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
    response = api_request("POST", "/simulate_disruptions/", json=[event])
    if response.status_code == 200:
        st.success("Disruption simulated!")
        # Fetch latest alerts and auto-generate GenAI plan
        alerts = requests.get("http://localhost:8000/alerts/").json().get("alerts", [])
        if alerts:
            latest_risk_report = alerts[-1].get("risk_report", [])
            with st.spinner("Getting GenAI plan for latest disruption..."):
                resp = api_request("POST", "/genai_plan/", json=latest_risk_report)
            st.header("GenAI Action Plan (Latest Disruption)")
            st.json(resp.json())
    else:
        st.error(response.json().get("detail", "Simulation failed."))

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
        
        # Fix: Check if action_plan is a list or dict and handle accordingly
        if isinstance(alert['action_plan'], dict):
            risk_score = alert['action_plan'].get('risk_score', 'N/A')
        elif isinstance(alert['action_plan'], list):
            # If it's a list, try to find risk_score in the first item if available
            if alert['action_plan'] and isinstance(alert['action_plan'][0], dict) and 'risk_score' in alert['action_plan'][0]:
                risk_score = alert['action_plan'][0]['risk_score']
            else:
                # If it's an empty list or doesn't contain risk_score information
                risk_score = 'N/A'
        else:
            risk_score = 'N/A'
            
        st.markdown(f"**Risk Score:** {risk_score}")
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
    risk_scores = []
    for a in alerts:
        if isinstance(a["action_plan"], dict) and a["action_plan"].get("risk_score") is not None:
            risk_scores.append(a["action_plan"].get("risk_score", 0))
        elif isinstance(a["action_plan"], list) and a["action_plan"] and isinstance(a["action_plan"][0], dict) and "risk_score" in a["action_plan"][0]:
            risk_scores.append(a["action_plan"][0]["risk_score"])
    
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
    shipments = requests.get("http://localhost:8000/shipments/").json().get("shipments", [])
    # Extract unique product_ids from risk reports for selection
    all_shipments = set()
    for item in shipments:
        all_shipments.add(item.get("product_id"))
    all_shipments = sorted(list(all_shipments))
except Exception:
    all_shipments = []

if all_shipments:
    product_id = st.selectbox("Select Shipment", all_shipments)
    new_location = st.text_input("New Current Location")
    new_status = st.selectbox("Status", ["in_transit", "rerouted", "delayed", "delivered"])
    if st.button("Update Shipment"):
        print(f"[FRONTEND] Updating shipment: {product_id}, new_location: {new_location}, new_status: {new_status}")
        update = {"product_id": product_id, "current_location": new_location, "status": new_status}
        response = api_request("POST", "/update_shipment/", json=update)
        print(f"[FRONTEND] Update Shipment API response: {response.status_code} {response.text}")
        if response.status_code == 200:
            st.write(response.json())
        else:
            st.error(response.json().get("detail", "Update failed."))
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
        response = api_request("POST", "/simulate_disruptions/", json=disruptions)
        st.json(response.json())
        # Fetch latest alerts and auto-generate GenAI plan
        alerts = requests.get("http://localhost:8000/alerts/").json().get("alerts", [])
        if alerts:
            latest_risk_report = alerts[-1].get("risk_report", [])
            with st.spinner("Getting GenAI plan for latest disruption..."):
                resp = api_request("POST", "/genai_plan/", json=latest_risk_report)
            st.header("GenAI Action Plan (Latest Disruption)")
            st.json(resp.json())
    except Exception as e:
        st.error(f"Invalid JSON or API error: {e}")

# --- Show Current Shipments and Status ---
st.header("Current Shipments")
try:
    shipments = requests.get("http://localhost:8000/shipments/").json().get("shipments", [])
    for item in shipments:
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
        update_resp = api_request("POST", "/update_shipment/", json=update)
        if update_resp.status_code == 200:
            st.write("Shipment updated:", update_resp.json())
        else:
            st.error(update_resp.json().get("detail", "Update failed."))
        # 2. Simulate disruption at new location
        disruption = [{
            "location": new_scenario_location,
            "event_type": "Flood",
            "severity": "High",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "source": "Simulated",
            "mode": "road"
        }]
        sim_resp = api_request("POST", "/simulate_disruptions/", json=disruption)
        if sim_resp.status_code == 200:
            st.write("Disruption simulated:", sim_resp.json())
        else:
            st.error(sim_resp.json().get("detail", "Simulation failed."))

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
    shipments = requests.get("http://localhost:8000/shipments/").json().get("shipments", [])
    for item in shipments:
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
    shipments = requests.get("http://localhost:8000/shipments/").json().get("shipments", [])
    # Build a DataFrame for all legs and current locations
    map_rows = []
    for item in shipments:
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
    shipments = requests.get("http://localhost:8000/shipments/").json().get("shipments", [])
    for item in shipments:
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

# --- Shipment Association and GPS Update (Traccar) ---
st.header("Associate Traccar Device with Shipment")
# Fetch Traccar devices from backend
traccar_devices = []
try:
    resp = api_request("GET", "/list_traccar_devices/")
    traccar_devices = resp.json().get("devices", [])
except Exception as e:
    print(f"[FRONTEND] Failed to fetch Traccar devices: {e}")

device_options = [f"{d['id']} - {d.get('name','')} (Last: {d.get('lastUpdate','N/A')})" for d in traccar_devices]
device_id_map = {f"{d['id']} - {d.get('name','')} (Last: {d.get('lastUpdate','N/A')})": d['id'] for d in traccar_devices}

try:
    shipments = requests.get("http://localhost:8000/shipments/").json().get("shipments", [])
    all_shipments = sorted([item["product_id"] for item in shipments])
except Exception:
    all_shipments = []

if all_shipments:
    assoc_product_id = st.selectbox("Select Shipment to Associate", all_shipments, key="assoc_pid")
    assoc_device_label = st.selectbox("Select Traccar Device", device_options, key="assoc_did") if device_options else st.text_input("Traccar Device ID", key="assoc_did_txt")
    assoc_device_id = device_id_map.get(assoc_device_label) if device_options else assoc_device_label
    if st.button("Associate Device", key="assoc_btn"):
        print(f"[FRONTEND] Associating device {assoc_device_id} with shipment {assoc_product_id}")
        resp = api_request("POST", "/associate_traccar_device/", json={"product_id": assoc_product_id, "device_id": assoc_device_id})
        st.write(resp.json())

st.header("Update Shipment Location via Traccar GPS")
update_gps_product_id = st.selectbox("Select Shipment for GPS Update", all_shipments, key="gps_pid2")
update_gps_device_label = st.selectbox("Select Traccar Device (optional)", ["(Use associated device)"] + device_options, key="gps_did2") if device_options else st.text_input("Traccar Device ID (leave blank to use associated)", key="gps_did2_txt")
update_gps_device_id = device_id_map.get(update_gps_device_label) if device_options and update_gps_device_label != "(Use associated device)" else None
if st.button("Update via Traccar GPS", key="update_gps_btn"):
    print(f"[FRONTEND] Updating shipment {update_gps_product_id} via Traccar device {update_gps_device_id}")
    payload = {"product_id": update_gps_product_id}
    if update_gps_device_id:
        payload["device_id"] = update_gps_device_id
    resp = api_request("POST", "/update_shipment_gps/", json=payload)
    st.write(resp.json())

if traccar_devices:
    st.header("Traccar Devices (Live)")
    for d in traccar_devices:
        st.markdown(f"**ID:** {d['id']} | **Name:** {d.get('name','')} | **Status:** {d.get('status','N/A')} | **Last Update:** {d.get('lastUpdate','N/A')}")
        pos = d.get('position')
        if pos:
            st.markdown(f"- **Lat/Lon:** {pos.get('latitude','N/A')}, {pos.get('longitude','N/A')} | **Speed:** {pos.get('speed','N/A')}")

# --- Admin: User Management ---
if is_admin:
    st.header("User Management (Admin Only)")
    search = st.text_input("Search users by email", key="user_search")
    page = st.number_input("Page", min_value=1, value=1, step=1, key="user_page")
    page_size = st.selectbox("Page Size", [10, 20, 50, 100], index=1, key="user_page_size")
    if st.button("List Users"):
        with st.spinner("Fetching users..."):
            params = {"page": page, "page_size": page_size}
            if search:
                params["search"] = search
            resp = api_request("GET", "/admin/users/", params=params)
        if resp.status_code == 200:
            data = resp.json()
            users = data.get("users", [])
            total = data.get("total", 0)
            st.write(f"Total users: {total} | Page {data.get('page', 1)} | Page size: {data.get('page_size', page_size)}")
            for u in users:
                st.write(u)
                if st.button(f"Delete User {u['id']}", key=f"del_{u['id']}"):
                    if st.confirm(f"Are you sure you want to delete user {u['email']}?"):
                        with st.spinner("Deleting user..."):
                            del_resp = api_request("POST", "/admin/user/delete/", json={"user_id": u["id"]})
                        if del_resp.status_code == 200:
                            st.success(f"User {u['email']} deleted.")
                        else:
                            st.error(del_resp.json().get("detail", "Delete failed."))
        else:
            st.error("Failed to fetch users.")
    st.markdown("---")

# --- Operator/Admin: Update Shipment via GPS ---
if is_operator:
    st.header("Update Shipment via GPS (Operator Only)")
    product_id = st.text_input("Product ID for GPS Update", key="gps_pid")
    device_id = st.text_input("Device ID", key="gps_did")
    if st.button("Update via GPS"):
        with st.spinner("Updating via GPS..."):
            payload = {"product_id": product_id, "device_id": device_id}
            resp = api_request("POST", "/update_shipment_gps/", json=payload)
        if resp.status_code == 200:
            st.write(resp.json())
        else:
            st.error(resp.json().get("detail", "GPS update failed."))
    st.markdown("---")

# --- Operator/Admin: Update Shipment via Provider ---
if is_operator:
    st.header("Update Shipment via Provider (Operator Only)")
    product_id = st.text_input("Product ID for Provider Update", key="prov_pid")
    provider = st.text_input("Provider Name", key="prov_name")
    provider_id = st.text_input("Provider ID", key="prov_id")
    if st.button("Update via Provider"):
        with st.spinner("Updating via provider..."):
            payload = {"product_id": product_id, "provider": provider, "provider_id": provider_id}
            resp = api_request("POST", "/update_shipment_provider/", json=payload)
        if resp.status_code == 200:
            st.write(resp.json())
        else:
            st.error(resp.json().get("detail", "Provider update failed."))
    st.markdown("---")

# --- Notification/Audit Log (if available) ---
if is_admin:
    st.header("Notification & Audit Log (Admin Only)")
    resp = api_request("GET", "/admin/audit_log/")
    if resp.status_code == 200:
        logs = resp.json().get("logs", [])
        for log in logs:
            st.write(log)
    else:
        st.info("No audit log endpoint or failed to fetch logs.")
    st.markdown("---")

# --- Backend Health Check ---
st.header("Backend Health Status")
resp = api_request("GET", "/healthz")
if resp.status_code == 200:
    st.success(f"Backend status: {resp.json().get('status')}")
else:
    st.error("Backend health check failed.")
st.markdown("---")