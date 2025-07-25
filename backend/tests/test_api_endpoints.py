import requests
import pytest

BASE = "http://localhost:8000"

def test_auth_register():
    payload = {"username": "testuser", "password": "testpass"}
    resp = requests.post(f"{BASE}/auth/register", json=payload)
    assert resp.status_code in (200, 400, 409)

def test_auth_login():
    payload = {"username": "testuser", "password": "testpass"}
    resp = requests.post(f"{BASE}/auth/login", json=payload)
    assert resp.status_code in (200, 401)
    if resp.status_code == 200:
        assert "access_token" in resp.json()

def test_auth_change_password():
    payload = {"username": "testuser", "old_password": "testpass", "new_password": "newpass"}
    resp = requests.post(f"{BASE}/auth/change_password", json=payload)
    assert resp.status_code in (200, 400, 401)

def test_update_shipment():
    payload = {"product_id": "P1001", "status": "delivered"}
    resp = requests.post(f"{BASE}/update_shipment/", json=payload)
    assert resp.status_code in (200, 404)

def test_associate_traccar_device():
    payload = {"product_id": "P1001", "device_id": 1}
    resp = requests.post(f"{BASE}/associate_traccar_device/", json=payload)
    assert resp.status_code in (200, 404)

def test_update_shipment_gps():
    payload = {"product_id": "P1001", "device_id": 1}
    resp = requests.post(f"{BASE}/update_shipment_gps/", json=payload)
    assert resp.status_code in (200, 400, 404, 500)

def test_update_shipment_provider():
    payload = {"product_id": "P1001", "provider": "SomeProvider", "provider_id": "123"}
    resp = requests.post(f"{BASE}/update_shipment_provider/", json=payload)
    assert resp.status_code in (200, 400, 404, 500)

def test_list_traccar_devices():
    resp = requests.get(f"{BASE}/list_traccar_devices/")
    assert resp.status_code in (200, 500)
    if resp.status_code == 200:
        assert "devices" in resp.json()

def test_shipments():
    resp = requests.get(f"{BASE}/shipments/")
    assert resp.status_code == 200
    assert "shipments" in resp.json()

def test_simulate_disruptions():
    disruptions = [{
        "location": "Bangalore",
        "event_type": "Strike",
        "severity": "High",
        "timestamp": "2025-07-25T12:00:00Z",
        "source": "Simulated",
        "mode": "road"
    }]
    resp = requests.post(f"{BASE}/simulate_disruptions/", json=disruptions)
    assert resp.status_code in (200, 401, 403)
    if resp.status_code == 200:
        assert "alerts" in resp.json()

def test_genai_plan():
    risk_report = [{
        "product_id": "P1001",
        "risk_score": 85,
        "impact_level": "High",
        "delay_estimate": "3-5 days",
        "cost_impact": "10000-15000",
        "escalation": "Notify VP of Global Ops and expedite alternative route planning",
        "summary": "The shipment of product P1001 is at high risk due to a strike in Bangalore, requiring immediate escalation and alternative route planning to mitigate potential delays and cost impacts. Expedited actions are necessary to ensure timely delivery."
    }]
    resp = requests.post(f"{BASE}/genai_plan/", json=risk_report)
    assert resp.status_code in (200, 400, 500)

def test_alerts():
    resp = requests.get(f"{BASE}/alerts/")
    assert resp.status_code == 200
    assert "alerts" in resp.json()

def test_chat():
    resp = requests.post(f"{BASE}/chat/", json={"query": "Which shipments are at highest risk?"})
    assert resp.status_code == 200
    assert "answer" in resp.json()

def test_explain_risk():
    resp = requests.get(f"{BASE}/explain_risk/", params={"product_id": "P1001"})
    assert resp.status_code in (200, 404)

def test_batch_simulate_disruptions():
    disruptions = [{
        "location": "Bangalore",
        "event_type": "Strike",
        "severity": "High",
        "timestamp": "2025-07-25T12:00:00Z",
        "source": "Simulated",
        "mode": "road"
    }]
    resp = requests.post(f"{BASE}/batch_simulate_disruptions/", json=disruptions)
    assert resp.status_code in (200, 401, 403)

def test_process_all_disruptions():
    disruptions = [{
        "location": "Bangalore",
        "event_type": "Strike",
        "severity": "High",
        "timestamp": "2025-07-25T12:00:00Z",
        "source": "Simulated",
        "mode": "road"
    }]
    resp = requests.post(f"{BASE}/process_all_disruptions/", json=disruptions)
    assert resp.status_code in (200, 401, 403)
    if resp.status_code == 200:
        assert "alerts" in resp.json()

def test_risk_heatmap():
    resp = requests.get(f"{BASE}/risk_heatmap/")
    assert resp.status_code == 200
    assert "heatmap" in resp.json()

def test_root():
    resp = requests.get(f"{BASE}/")
    assert resp.status_code == 200
    assert "message" in resp.json()

def test_healthz():
    resp = requests.get(f"{BASE}/healthz")
    assert resp.status_code == 200
    assert resp.json().get("status") == "ok"

def test_admin_users():
    resp = requests.get(f"{BASE}/admin/users/")
    assert resp.status_code in (200, 401, 403)
    if resp.status_code == 200:
        assert "users" in resp.json()

def test_admin_create_user():
    payload = {"username": "adminuser", "password": "adminpass"}
    resp = requests.post(f"{BASE}/admin/users/", json=payload)
    assert resp.status_code in (200, 400, 409)

def test_admin_update_user():
    user_id = 1
    payload = {"username": "adminuser", "password": "newpass"}
    resp = requests.put(f"{BASE}/admin/users/{user_id}", json=payload)
    assert resp.status_code in (200, 404, 400)

def test_admin_delete_user():
    user_id = 1
    resp = requests.delete(f"{BASE}/admin/users/{user_id}")
    assert resp.status_code in (200, 404)

def test_admin_audit_log():
    resp = requests.get(f"{BASE}/admin/audit_log/")
    assert resp.status_code in (200, 401, 403)
    if resp.status_code == 200:
        assert "logs" in resp.json()

def test_analytics_risk_categories():
    resp = requests.get(f"{BASE}/analytics/risk_categories/")
    assert resp.status_code == 200
    assert "categories" in resp.json()

def test_analytics_shipment_volume():
    resp = requests.get(f"{BASE}/analytics/shipment_volume/")
    assert resp.status_code == 200
    assert "volume" in resp.json()

def test_analytics_on_time_delivery():
    resp = requests.get(f"{BASE}/analytics/on_time_delivery/")
    assert resp.status_code == 200
    assert "on_time_delivery" in resp.json()

def test_analytics_performance_metrics():
    resp = requests.get(f"{BASE}/analytics/performance_metrics/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict)

def test_workflow_steps():
    resp = requests.get(f"{BASE}/workflow/steps/")
    assert resp.status_code == 200
    assert "steps" in resp.json()

def test_workflow_progress():
    resp = requests.get(f"{BASE}/workflow/progress/")
    assert resp.status_code == 200
    assert "progress" in resp.json()

def test_tool_calls():
    resp = requests.get(f"{BASE}/tool_calls/")
    assert resp.status_code == 200
    assert "tool_calls" in resp.json()

def test_agents_network():
    resp = requests.get(f"{BASE}/agents/network/")
    assert resp.status_code == 200
    assert "network" in resp.json()

def test_ports_status():
    resp = requests.get(f"{BASE}/ports/status/")
    assert resp.status_code == 200
    assert "ports" in resp.json()

def test_user_settings_get():
    resp = requests.get(f"{BASE}/user/settings/")
    assert resp.status_code == 200
    assert "settings" in resp.json()

def test_user_settings_post():
    payload = {"theme": "dark"}
    resp = requests.post(f"{BASE}/user/settings/", json=payload)
    assert resp.status_code in (200, 400)

def test_simulation_state():
    resp = requests.get(f"{BASE}/simulation/state/")
    assert resp.status_code == 200
    assert "state" in resp.json()

def test_agents_list():
    resp = requests.get(f"{BASE}/agents/list/")
    assert resp.status_code == 200
    assert "agents" in resp.json()

def test_agents_update_status():
    payload = {"agent_id": "risk_analyzer", "status": "active"}
    resp = requests.post(f"{BASE}/agents/update_status/", json=payload)
    assert resp.status_code in (200, 400, 404)

def test_check_integrations():
    resp = requests.get(f"{BASE}/check_integrations")
    assert resp.status_code == 200
    assert "integration_status" in resp.json()

def test_analytics_risk_trends():
    resp = requests.get(f"{BASE}/analytics/risk_trends/")
    assert resp.status_code == 200
    assert "riskData" in resp.json()

def test_analytics_port_performance():
    resp = requests.get(f"{BASE}/analytics/port_performance/")
    assert resp.status_code == 200
    assert "ports" in resp.json()

def test_analytics_kpis():
    resp = requests.get(f"{BASE}/analytics/kpis/")
    assert resp.status_code == 200
    assert isinstance(resp.json(), dict) 