import pytest
import requests
import json
import time

BASE_URL = "http://localhost:8000"

REG_EMAIL = f"testuser_{int(time.time())}@example.com"
REG_PASS = "TestPassword123!"

OP_EMAIL = f"operator_{int(time.time())}@example.com"
OP_PASS = "OperatorPass123!"

VIEW_EMAIL = f"viewer_{int(time.time())}@example.com"
VIEW_PASS = "ViewerPass123!"

@pytest.mark.parametrize("endpoint", ["/", "/alerts/"])
def test_backend_endpoints(endpoint):
    url = BASE_URL + endpoint
    response = requests.get(url)
    assert response.status_code == 200, f"{endpoint} did not return 200 OK"


@pytest.mark.parametrize("mode", ["air", "sea", "road"])
def test_fetch_events(mode):
    url = f"{BASE_URL}/fetch_events/{mode}"
    response = requests.get(url)
    assert response.status_code == 200
    data = response.json()
    assert "events" in data
    assert isinstance(data["events"], list)


def test_analyze_risk():
    # Use a sample event
    event = {
        "location": "Bangalore Port",
        "event_type": "Strike",
        "severity": "High",
        "timestamp": "2024-06-01T12:00:00Z",
        "source": "Simulated",
        "mode": "road"
    }
    url = f"{BASE_URL}/analyze_risk/"
    response = requests.post(url, json=event)
    assert response.status_code == 200
    data = response.json()
    assert "risk_report" in data
    assert isinstance(data["risk_report"], list)


def test_analyze_risk_multiple():
    disruptions = [
        {
            "location": "Hubli",
            "event_type": "Flood",
            "severity": "High",
            "timestamp": "2024-06-10T10:00:00Z",
            "source": "Simulated",
            "mode": "road"
        },
        {
            "location": "Nagpur",
            "event_type": "Strike",
            "severity": "Medium",
            "timestamp": "2024-06-11T12:00:00Z",
            "source": "Simulated",
            "mode": "road"
        }
    ]
    url = f"{BASE_URL}/analyze_risk/"
    response = requests.post(url, json=disruptions)
    assert response.status_code == 200
    data = response.json()
    assert "risk_report" in data
    assert isinstance(data["risk_report"], list)
    assert len(data["risk_report"]) > 0

def test_update_shipment():
    update = {
        "product_id": "P1001",
        "current_location": "Pune",
        "status": "rerouted"
    }
    url = f"{BASE_URL}/update_shipment/"
    response = requests.post(url, json=update)
    assert response.status_code == 200
    data = response.json()
    assert "updated_shipment" in data
    assert data["updated_shipment"]["product_id"] == "P1001"
    assert data["updated_shipment"]["current_location"] == "Pune"
    assert data["updated_shipment"]["status"] == "rerouted"

def test_simulate_disruptions():
    disruptions = [
        {
            "location": "Singapore",
            "event_type": "Port Closure",
            "severity": "High",
            "timestamp": "2024-06-18T08:00:00Z",
            "source": "Simulated",
            "mode": "sea"
        },
        {
            "location": "Kolkata",
            "event_type": "Protest",
            "severity": "Medium",
            "timestamp": "2024-06-17T09:00:00Z",
            "source": "Simulated",
            "mode": "road"
        }
    ]
    url = f"{BASE_URL}/simulate_disruptions/"
    response = requests.post(url, json=disruptions)
    assert response.status_code == 200
    data = response.json()
    assert "alerts" in data
    assert isinstance(data["alerts"], list)
    assert len(data["alerts"]) == 2


def test_genai_plan():
    # Use a sample risk report
    risk_report = [{
        "product_id": "P1001",
        "vendor": "Vendor_001",
        "delay_estimate": "2-5 days",
        "impact_level": "High",
        "risk_score": 90
    }]
    url = f"{BASE_URL}/genai_plan/"
    response = requests.post(url, json=risk_report)
    assert response.status_code == 200
    data = response.json()
    assert "action_plan" in data
    assert isinstance(data["action_plan"], list)

def test_user_registration_and_login():
    # Register user
    reg_url = f"{BASE_URL}/auth/register"
    reg_data = {"email": REG_EMAIL, "password": REG_PASS, "role": "admin"}
    reg_resp = requests.post(reg_url, json=reg_data)
    assert reg_resp.status_code in (201, 400), f"Registration failed: {reg_resp.text}"
    # 400 is allowed if user already exists

    # Login user
    login_url = f"{BASE_URL}/auth/jwt/login"
    login_data = {"username": REG_EMAIL, "password": REG_PASS}
    login_resp = requests.post(login_url, data=login_data)
    assert login_resp.status_code == 200, f"Login failed: {login_resp.text}"
    token = login_resp.json().get("access_token")
    assert token, "No access token returned"

    # Access protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    protected_url = f"{BASE_URL}/protected-admin/"
    protected_resp = requests.get(protected_url, headers=headers)
    assert protected_resp.status_code == 200, f"Protected endpoint failed: {protected_resp.text}"

def test_operator_and_viewer_roles():
    reg_url = f"{BASE_URL}/auth/register"
    login_url = f"{BASE_URL}/auth/jwt/login"

    # Register operator
    op_data = {"email": OP_EMAIL, "password": OP_PASS, "role": "operator"}
    op_resp = requests.post(reg_url, json=op_data)
    assert op_resp.status_code in (201, 400)
    op_login = requests.post(login_url, data={"username": OP_EMAIL, "password": OP_PASS})
    assert op_login.status_code == 200
    op_token = op_login.json().get("access_token")
    assert op_token
    op_headers = {"Authorization": f"Bearer {op_token}"}

    # Operator: should succeed on /protected-operator/ and /protected-viewer/, fail on /protected-admin/
    assert requests.get(f"{BASE_URL}/protected-operator/", headers=op_headers).status_code == 200
    assert requests.get(f"{BASE_URL}/protected-viewer/", headers=op_headers).status_code == 200
    assert requests.get(f"{BASE_URL}/protected-admin/", headers=op_headers).status_code == 403

    # Register viewer
    view_data = {"email": VIEW_EMAIL, "password": VIEW_PASS, "role": "viewer"}
    view_resp = requests.post(reg_url, json=view_data)
    assert view_resp.status_code in (201, 400)
    view_login = requests.post(login_url, data={"username": VIEW_EMAIL, "password": VIEW_PASS})
    assert view_login.status_code == 200
    view_token = view_login.json().get("access_token")
    assert view_token
    view_headers = {"Authorization": f"Bearer {view_token}"}

    # Viewer: should succeed on /protected-viewer/, fail on /protected-operator/ and /protected-admin/
    assert requests.get(f"{BASE_URL}/protected-viewer/", headers=view_headers).status_code == 200
    assert requests.get(f"{BASE_URL}/protected-operator/", headers=view_headers).status_code == 403
    assert requests.get(f"{BASE_URL}/protected-admin/", headers=view_headers).status_code == 403 