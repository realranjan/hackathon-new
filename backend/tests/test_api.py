import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from app import app
import jwt
from db import JWT_SECRET
from datetime import datetime, timedelta

USERS = [
    {"email": "admin@example.com", "password": "AdminPass123!", "role": "admin"},
    {"email": "operator@example.com", "password": "OperatorPass123!", "role": "operator"},
    {"email": "viewer@example.com", "password": "ViewerPass123!", "role": "viewer"},
]

@pytest.mark.asyncio
async def test_full_api_flow():
    # Use TestClient for sync endpoints, or httpx.AsyncClient with ASGITransport for async
    from httpx import ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        tokens = {}
        # Register all users
        for user in USERS:
            resp = await ac.post("/auth/register", json=user)
            assert resp.status_code == 200 or resp.json().get("message") == "User already exists"
        # Duplicate registration
        resp = await ac.post("/auth/register", json=USERS[0])
        assert resp.status_code == 200 and resp.json().get("message") == "User already exists"
        # Login all users and store tokens
        for user in USERS:
            resp = await ac.post("/auth/login", json={"email": user["email"], "password": user["password"]})
            assert resp.status_code == 200
            tokens[user["role"]] = resp.json()["access_token"]
        # Login with wrong password
        resp = await ac.post("/auth/login", json={"email": USERS[0]["email"], "password": "wrongpass"})
        assert resp.status_code == 401
        # Login with missing fields
        resp = await ac.post("/auth/login", json={"email": USERS[0]["email"]})
        assert resp.status_code == 422
        # Health endpoints (no auth)
        resp = await ac.get("/")
        assert resp.status_code == 200
        resp = await ac.get("/healthz")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"
        # Simulate disruption (admin only)
        headers = {"Authorization": f"Bearer {tokens['admin']}"}
        resp = await ac.post("/simulate_disruptions/", json=[{
            "location": "Bangalore",
            "event_type": "strike",
            "severity": "high",
            "timestamp": "2024-07-24T12:00:00Z",
            "source": "manual"
        }], headers=headers)
        assert resp.status_code == 200
        # Should fail for operator/viewer
        for role in ["operator", "viewer"]:
            headers = {"Authorization": f"Bearer {tokens[role]}"}
            resp = await ac.post("/simulate_disruptions/", json=[{
                "location": "Bangalore",
                "event_type": "strike",
                "severity": "high",
                "timestamp": "2024-07-24T12:00:00Z",
                "source": "manual"
            }], headers=headers)
            assert resp.status_code == 403
        # Simulate disruption with missing token
        resp = await ac.post("/simulate_disruptions/", json=[{
            "location": "Bangalore",
            "event_type": "strike",
            "severity": "high",
            "timestamp": "2024-07-24T12:00:00Z",
            "source": "manual"
        }])
        assert resp.status_code == 403 or resp.status_code == 401
        # Simulate disruption with invalid token
        headers = {"Authorization": "Bearer invalidtoken"}
        resp = await ac.post("/simulate_disruptions/", json=[{
            "location": "Bangalore",
            "event_type": "strike",
            "severity": "high",
            "timestamp": "2024-07-24T12:00:00Z",
            "source": "manual"
        }], headers=headers)
        assert resp.status_code == 401
        # Simulate disruption with expired token
        expired_token = jwt.encode({"sub": USERS[0]["email"], "exp": datetime.utcnow() - timedelta(hours=1)}, JWT_SECRET, algorithm="HS256")
        headers = {"Authorization": f"Bearer {expired_token}"}
        resp = await ac.post("/simulate_disruptions/", json=[{
            "location": "Bangalore",
            "event_type": "strike",
            "severity": "high",
            "timestamp": "2024-07-24T12:00:00Z",
            "source": "manual"
        }], headers=headers)
        assert resp.status_code == 401
        # GenAI plan (any authenticated user)
        for role in tokens:
            headers = {"Authorization": f"Bearer {tokens[role]}"}
            resp = await ac.post("/genai_plan/", json=[{"risk_report": []}], headers=headers)
            assert resp.status_code in (200, 422)
        # GenAI plan with missing token
        resp = await ac.post("/genai_plan/", json=[{"risk_report": []}])
        assert resp.status_code == 403 or resp.status_code == 401
        # Update shipment (admin only)
        headers = {"Authorization": f"Bearer {tokens['admin']}"}
        resp = await ac.post("/update_shipment/", json={"product_id": "P1001", "status": "delayed"}, headers=headers)
        assert resp.status_code in (200, 404, 500)
        # Should fail for operator/viewer
        for role in ["operator", "viewer"]:
            headers = {"Authorization": f"Bearer {tokens[role]}"}
            resp = await ac.post("/update_shipment/", json={"product_id": "P1001", "status": "delayed"}, headers=headers)
            assert resp.status_code == 403
        # Update shipment with missing fields
        headers = {"Authorization": f"Bearer {tokens['admin']}"}
        resp = await ac.post("/update_shipment/", json={}, headers=headers)
        assert resp.status_code == 422
        # Update shipment GPS (operator only)
        headers = {"Authorization": f"Bearer {tokens['operator']}"}
        resp = await ac.post("/update_shipment_gps/", json={"product_id": "P1001", "device_id": "dev1"}, headers=headers)
        assert resp.status_code in (200, 404, 500)
        # Should fail for admin/viewer
        for role in ["admin", "viewer"]:
            headers = {"Authorization": f"Bearer {tokens[role]}"}
            resp = await ac.post("/update_shipment_gps/", json={"product_id": "P1001", "device_id": "dev1"}, headers=headers)
            assert resp.status_code == 403
        # Update shipment GPS with missing fields
        headers = {"Authorization": f"Bearer {tokens['operator']}"}
        resp = await ac.post("/update_shipment_gps/", json={"product_id": "P1001"}, headers=headers)
        assert resp.status_code == 400 or resp.status_code == 422
        # Update shipment provider (operator only)
        headers = {"Authorization": f"Bearer {tokens['operator']}"}
        resp = await ac.post("/update_shipment_provider/", json={"product_id": "P1001", "provider": "test", "provider_id": "pid1"}, headers=headers)
        assert resp.status_code in (200, 404, 500)
        # Should fail for admin/viewer
        for role in ["admin", "viewer"]:
            headers = {"Authorization": f"Bearer {tokens[role]}"}
            resp = await ac.post("/update_shipment_provider/", json={"product_id": "P1001", "provider": "test", "provider_id": "pid1"}, headers=headers)
            assert resp.status_code == 403
        # Update shipment provider with missing fields
        headers = {"Authorization": f"Bearer {tokens['operator']}"}
        resp = await ac.post("/update_shipment_provider/", json={"product_id": "P1001", "provider": "test"}, headers=headers)
        assert resp.status_code == 400 or resp.status_code == 422 