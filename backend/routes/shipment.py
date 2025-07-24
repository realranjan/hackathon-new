import os
from fastapi import APIRouter, Request, Body, HTTPException, Depends
from models import ShipmentUpdateRequest, ShipmentUpdateResponse
from auth import get_current_user_role
from utils.data_loader import get_latest_gps_position, update_shipment_location_by_gps, get_latest_location_from_provider
import json
from typing import Any, Dict, List

shipment_router = APIRouter()

# Helper for absolute inventory path
INVENTORY_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'inventory.json'))

@shipment_router.post("/update_shipment/", response_model=ShipmentUpdateResponse)
async def update_shipment(request: Request, update: ShipmentUpdateRequest, user=Depends(get_current_user_role("admin"))):
    print(f"[API] /update_shipment/ called for product_id={update.product_id}")
    product_id = update.product_id
    if not product_id:
        raise HTTPException(status_code=400, detail="Missing product_id in update.")
    inventory_path = INVENTORY_PATH
    if not os.path.exists(inventory_path):
        raise HTTPException(status_code=500, detail="Inventory file not found.")
    with open(inventory_path) as f:
        inventory = json.load(f)
    found = False
    update_dict = update.dict(exclude_unset=True)
    for item in inventory:
        if item.get("product_id") == product_id:
            found = True
            for k, v in update_dict.items():
                if k != "product_id":
                    item[k] = v
            break
    if not found:
        raise HTTPException(status_code=404, detail="Shipment not found.")
    with open(inventory_path, "w") as f:
        json.dump(inventory, f, indent=2)
    return {"updated_shipment": update_dict}

@shipment_router.post("/associate_traccar_device/")
async def associate_traccar_device(request: Request, payload: dict = Body(...), user=Depends(get_current_user_role("admin"))):
    """Associate a Traccar device_id with a shipment (product_id)."""
    product_id = payload.get("product_id")
    device_id = payload.get("device_id")
    print(f"[API] /associate_traccar_device/ called for product_id={product_id}, device_id={device_id}")
    inventory_path = INVENTORY_PATH
    if not os.path.exists(inventory_path):
        raise HTTPException(status_code=500, detail="Inventory file not found.")
    with open(inventory_path) as f:
        inventory = json.load(f)
    found = False
    for item in inventory:
        if item.get("product_id") == product_id:
            item["traccar_device_id"] = device_id
            found = True
            break
    if not found:
        raise HTTPException(status_code=404, detail="Shipment not found.")
    with open(inventory_path, "w") as f:
        json.dump(inventory, f, indent=2)
    return {"message": f"Device {device_id} associated with shipment {product_id}"}

@shipment_router.post("/update_shipment_gps/")
async def update_shipment_gps(request: Request, payload: dict = Body(...), user=Depends(get_current_user_role("operator"))):
    product_id = payload.get("product_id")
    device_id = payload.get("device_id")
    print(f"[API] /update_shipment_gps/ called for product_id={product_id}, device_id={device_id}")
    inventory_path = INVENTORY_PATH
    if not os.path.exists(inventory_path):
        raise HTTPException(status_code=500, detail="Inventory file not found.")
    with open(inventory_path) as f:
        inventory = json.load(f)
    # If device_id is not provided, try to get it from the shipment
    if not device_id:
        for item in inventory:
            if item.get("product_id") == product_id:
                device_id = item.get("traccar_device_id")
                break
    if not device_id:
        raise HTTPException(status_code=400, detail="No device_id provided or associated with this shipment.")
    # Fetch latest GPS from Traccar demo server
    import requests
    traccar_api = os.getenv("TRACCAR_API", "https://demo.traccar.org/api")
    traccar_user = os.getenv("TRACCAR_USER")
    traccar_pass = os.getenv("TRACCAR_PASS")
    try:
        resp = requests.get(f"{traccar_api}/positions?deviceId={device_id}", auth=(traccar_user, traccar_pass))
        data = resp.json()
        if data:
            lat, lon = data[0]['latitude'], data[0]['longitude']
            print(f"[API] Traccar GPS: lat={lat}, lon={lon}")
        else:
            raise HTTPException(status_code=404, detail="No GPS position found for device.")
    except Exception as e:
        print(f"[API] Traccar fetch failed: {e}")
        raise HTTPException(status_code=500, detail=f"Traccar fetch failed: {e}")
    # Reverse geocode and update shipment location
    from utils.data_loader import update_shipment_location_by_gps
    city = update_shipment_location_by_gps(product_id, lat, lon, inventory_path)
    if not city:
        raise HTTPException(status_code=500, detail="Failed to update shipment location.")
    return {"product_id": product_id, "device_id": device_id, "lat": lat, "lon": lon, "current_location": city}

@shipment_router.post("/update_shipment_provider/")
async def update_shipment_provider(request: Request, payload: dict = Body(...), user=Depends(get_current_user_role("operator"))):
    print(f"[API] /update_shipment_provider/ called for product_id={payload.get('product_id')}, provider={payload.get('provider')}, provider_id={payload.get('provider_id')}")
    try:
        product_id = payload.get("product_id")
        provider = payload.get("provider")
        provider_id = payload.get("provider_id")
        if not product_id or not provider or not provider_id:
            raise HTTPException(status_code=400, detail="Missing product_id, provider, or provider_id.")
        lat, lon = get_latest_location_from_provider(product_id, provider, provider_id)
        if lat is None or lon is None:
            raise HTTPException(status_code=404, detail="No location found from provider.")
        city = update_shipment_location_by_gps(product_id, lat, lon)
        if not city:
            raise HTTPException(status_code=500, detail="Failed to update shipment location.")
        return {"product_id": product_id, "provider": provider, "provider_id": provider_id, "lat": lat, "lon": lon, "current_location": city}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Provider update failed: {e}")

@shipment_router.get("/list_traccar_devices/")
async def list_traccar_devices(user=Depends(get_current_user_role("operator"))):
    import requests
    traccar_api = os.getenv("TRACCAR_API", "https://demo.traccar.org/api")
    traccar_user = os.getenv("TRACCAR_USER")
    traccar_pass = os.getenv("TRACCAR_PASS")
    try:
        resp = requests.get(f"{traccar_api}/devices", auth=(traccar_user, traccar_pass))
        devices = resp.json()
        # Optionally fetch last positions for each device
        positions = {}
        pos_resp = requests.get(f"{traccar_api}/positions", auth=(traccar_user, traccar_pass))
        for pos in pos_resp.json():
            positions[pos["deviceId"]] = pos
        device_list = []
        for dev in devices:
            dev_info = {
                "id": dev.get("id"),
                "name": dev.get("name"),
                "uniqueId": dev.get("uniqueId"),
                "status": dev.get("status"),
                "lastUpdate": dev.get("lastUpdate"),
                "position": positions.get(dev.get("id"))
            }
            device_list.append(dev_info)
        return {"devices": device_list}
    except Exception as e:
        print(f"[API] list_traccar_devices failed: {e}")
        return {"devices": [], "error": str(e)} 