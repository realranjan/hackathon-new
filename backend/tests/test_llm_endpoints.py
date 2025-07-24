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

if __name__ == "__main__":
    test_chat()
    test_explain_risk()
    test_batch_simulate()
    test_risk_heatmap() 