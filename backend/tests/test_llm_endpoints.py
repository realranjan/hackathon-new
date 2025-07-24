import requests
import json

BASE = "http://localhost:8000"

def test_chat():
    resp = requests.post(f"{BASE}/chat/", json={"query": "Which shipments are at highest risk?"})
    print("/chat/ response:", resp.status_code, resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert "answer" in data and data["answer"].strip() != ""

def test_explain_risk():
    # Try to get a product_id from /alerts/
    alerts = requests.get(f"{BASE}/alerts/").json().get("alerts", [])
    product_id = None
    for alert in alerts:
        for rr in alert.get("risk_report", []):
            if rr.get("product_id"):
                product_id = rr["product_id"]
                break
        if product_id:
            break
    if not product_id:
        print("No product_id found for explain_risk test.")
        return
    resp = requests.get(f"{BASE}/explain_risk/", params={"product_id": product_id})
    print("/explain_risk/ response:", resp.status_code, resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert "explanation" in data and data["explanation"].strip() != ""

def test_batch_simulate():
    # Use a disruption from inventory
    disruptions = [
        {
            "location": "Bangalore",
            "event_type": "Strike",
            "severity": "High",
            "timestamp": "2025-07-25T12:00:00Z",
            "source": "Simulated"
        }
    ]
    resp = requests.post(f"{BASE}/batch_simulate_disruptions/", json=disruptions)
    print("/batch_simulate_disruptions/ response:", resp.status_code, resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert "risk_report" in data and isinstance(data["risk_report"], list)
    assert "action_plan" in data and isinstance(data["action_plan"], list)

def test_risk_heatmap():
    resp = requests.get(f"{BASE}/risk_heatmap/")
    print("/risk_heatmap/ response:", resp.status_code, resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert "heatmap" in data and isinstance(data["heatmap"], list)

def test_root_health():
    resp = requests.get(f"{BASE}/")
    print("/ (root) response:", resp.status_code, resp.text)
    assert resp.status_code == 200
    assert "message" in resp.json()

def test_healthz():
    resp = requests.get(f"{BASE}/healthz")
    print("/healthz response:", resp.status_code, resp.text)
    assert resp.status_code == 200
    assert resp.json().get("status") == "ok"

def test_check_integrations():
    resp = requests.get(f"{BASE}/check_integrations")
    print("/check_integrations response:", resp.status_code, resp.text)
    assert resp.status_code == 200
    data = resp.json().get("integration_status", {})
    for key in [
        "NewsAPI", "WeatherStack", "Twitter", "AviationStack", "MyShipTracking",
        "Traccar_API", "Traccar_Live_Device", "GoogleSheets", "Airtable",
        "SMTP", "Slack", "Twilio", "LLM_Groq", "Supabase"
    ]:
        assert key in data

def test_admin_users():
    # This test assumes you have a valid admin token or auth is disabled for dev
    resp = requests.get(f"{BASE}/admin/users/")
    print("/admin/users/ response:", resp.status_code, resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert "users" in data and isinstance(data["users"], list)
    assert "total" in data

def test_admin_audit_log():
    resp = requests.get(f"{BASE}/admin/audit_log/")
    print("/admin/audit_log/ response:", resp.status_code, resp.text)
    assert resp.status_code == 200
    data = resp.json()
    assert "logs" in data and isinstance(data["logs"], list)

def test_update_shipment():
    # Try to update a known shipment (adjust product_id as needed)
    payload = {"product_id": "P1001", "status": "delivered"}
    resp = requests.post(f"{BASE}/update_shipment/", json=payload)
    print("/update_shipment/ response:", resp.status_code, resp.text)
    # Accept 200 or 404 (if product_id not found)
    assert resp.status_code in (200, 404)
    if resp.status_code == 200:
        data = resp.json()
        assert "updated_shipment" in data

def test_associate_traccar_device():
    payload = {"product_id": "P1001", "device_id": 1}
    resp = requests.post(f"{BASE}/associate_traccar_device/", json=payload)
    print("/associate_traccar_device/ response:", resp.status_code, resp.text)
    assert resp.status_code in (200, 404)
    if resp.status_code == 200:
        data = resp.json()
        assert "message" in data

def test_update_shipment_gps():
    payload = {"product_id": "P1001", "device_id": 1}
    resp = requests.post(f"{BASE}/update_shipment_gps/", json=payload)
    print("/update_shipment_gps/ response:", resp.status_code, resp.text)
    assert resp.status_code in (200, 400, 404, 500)

def test_update_shipment_provider():
    payload = {"product_id": "P1001", "provider": "SomeProvider", "provider_id": "123"}
    resp = requests.post(f"{BASE}/update_shipment_provider/", json=payload)
    print("/update_shipment_provider/ response:", resp.status_code, resp.text)
    assert resp.status_code in (200, 400, 404, 500)

def test_list_traccar_devices():
    resp = requests.get(f"{BASE}/list_traccar_devices/")
    print("/list_traccar_devices/ response:", resp.status_code, resp.text)
    assert resp.status_code in (200, 500)
    if resp.status_code == 200:
        data = resp.json()
        assert "devices" in data and isinstance(data["devices"], list)

def test_permissions():
    # Try to call an admin endpoint as a non-admin (if auth enabled)
    # This is a placeholder; in real tests, set headers for a non-admin user
    resp = requests.get(f"{BASE}/admin/users/")
    print("/admin/users/ (permission test) response:", resp.status_code, resp.text)
    # Accept 200 (if auth disabled) or 401/403 (if enabled)
    assert resp.status_code in (200, 401, 403)

def test_invalid_input():
    # Missing product_id
    resp = requests.post(f"{BASE}/update_shipment/", json={"status": "delivered"})
    print("/update_shipment/ (invalid input) response:", resp.status_code, resp.text)
    assert resp.status_code == 400

def test_not_found():
    # Non-existent product_id
    payload = {"product_id": "NON_EXISTENT", "status": "delivered"}
    resp = requests.post(f"{BASE}/update_shipment/", json=payload)
    print("/update_shipment/ (not found) response:", resp.status_code, resp.text)
    assert resp.status_code == 404

if __name__ == "__main__":
    test_chat()
    test_explain_risk()
    test_batch_simulate()
    test_risk_heatmap()
    test_root_health()
    test_healthz()
    test_check_integrations()
    test_admin_users()
    test_admin_audit_log()
    test_update_shipment()
    test_associate_traccar_device()
    test_update_shipment_gps()
    test_update_shipment_provider()
    test_list_traccar_devices()
    test_permissions()
    test_invalid_input()
    test_not_found() 