from fastapi import APIRouter, Request, Body, HTTPException, Depends
from models import ShipmentUpdateRequest, ShipmentUpdateResponse
from auth import get_current_user_role
from utils.data_loader import get_latest_gps_position, update_shipment_location_by_gps, get_latest_location_from_provider
import os
import json
from typing import Any, Dict, List

shipment_router = APIRouter()

@shipment_router.post("/update_shipment/", response_model=ShipmentUpdateResponse)
async def update_shipment(request: Request, update: ShipmentUpdateRequest, user=Depends(get_current_user_role("admin"))):
    product_id = update.product_id
    if not product_id:
        raise HTTPException(status_code=400, detail="Missing product_id in update.")
    inventory_path = "data/inventory.json"
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

@shipment_router.post("/update_shipment_gps/")
async def update_shipment_gps(request: Request, payload: dict = Body(...), user=Depends(get_current_user_role("operator"))):
    try:
        product_id = payload.get("product_id")
        device_id = payload.get("device_id")
        if not product_id or not device_id:
            raise HTTPException(status_code=400, detail="Missing product_id or device_id.")
        lat, lon = get_latest_gps_position(device_id)
        if lat is None or lon is None:
            raise HTTPException(status_code=404, detail="No GPS position found for device.")
        city = update_shipment_location_by_gps(product_id, lat, lon)
        if not city:
            raise HTTPException(status_code=500, detail="Failed to update shipment location.")
        return {"product_id": product_id, "device_id": device_id, "lat": lat, "lon": lon, "current_location": city}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"GPS update failed: {e}")

@shipment_router.post("/update_shipment_provider/")
async def update_shipment_provider(request: Request, payload: dict = Body(...), user=Depends(get_current_user_role("operator"))):
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