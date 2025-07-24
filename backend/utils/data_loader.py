import pandas as pd
import json
import os
from dotenv import load_dotenv
import logging
import requests

load_dotenv()

# --- Real-Time GPS Tracking Integration (Traccar Example) ---
TRACCAR_API = os.getenv("TRACCAR_API", "http://localhost:8082/api")
TRACCAR_USER = os.getenv("TRACCAR_USER", "demo")
TRACCAR_PASS = os.getenv("TRACCAR_PASS", "demo")
TRACCAR_TOKEN = os.getenv("TRACCAR_TOKEN")

# Example: get_latest_gps_position(device_id) returns (lat, lon)
def get_latest_gps_position(device_id):
    """Fetch the latest GPS position for a device from Traccar using token auth if available."""
    try:
        headers = {}
        auth = None
        if TRACCAR_TOKEN:
            headers["Authorization"] = f"Bearer {TRACCAR_TOKEN}"
        else:
            auth = (TRACCAR_USER, TRACCAR_PASS)
        resp = requests.get(
            f"{TRACCAR_API}/positions?deviceId={device_id}",
            headers=headers,
            auth=auth
        )
        data = resp.json()
        if data:
            lat, lon = data[0]['latitude'], data[0]['longitude']
            return lat, lon
    except Exception as e:
        logging.error(f"Traccar GPS fetch failed: {e}")
    return None, None

# Example: update_shipment_location_by_gps(product_id, lat, lon)
def update_shipment_location_by_gps(product_id, lat, lon, inventory_path="data/inventory.json"):
    """Update a shipment's current_location in inventory.json based on GPS coordinates (reverse geocode to city/port)."""
    try:
        # Use OpenStreetMap Nominatim for reverse geocoding
        resp = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}")
        city = None
        if resp.status_code == 200:
            data = resp.json()
            city = data.get("address", {}).get("city") or data.get("address", {}).get("town") or data.get("address", {}).get("village") or data.get("display_name")
        if not city:
            city = f"({lat:.2f},{lon:.2f})"
        # Update inventory
        with open(inventory_path) as f:
            inventory = json.load(f)
        for item in inventory:
            if item.get("product_id") == product_id:
                item["current_location"] = city
                break
        with open(inventory_path, "w") as f:
            json.dump(inventory, f, indent=2)
        return city
    except Exception as e:
        logging.error(f"Failed to update shipment location by GPS: {e}")
        return None

# --- Provider-Agnostic Location Fetching ---
def get_latest_location_from_provider(product_id, provider, provider_id=None, **kwargs):
    """
    Fetch the latest location for a shipment from the specified provider.
    Supported providers: 'traccar', 'project44' (sample), can be extended.
    provider_id: device_id for Traccar, shipmentId for project44, etc.
    """
    if provider == "traccar":
        return get_latest_gps_position(provider_id)
    elif provider == "project44":
        # Sample project44 integration (mock token, endpoint)
        P44_API = os.getenv("P44_API", "https://api.project44.com/v4")
        P44_TOKEN = os.getenv("P44_TOKEN", "demo_token")
        headers = {"Authorization": f"Bearer {P44_TOKEN}"}
        try:
            resp = requests.get(f"{P44_API}/shipments/{provider_id}/locations", headers=headers)
            data = resp.json()
            if data and data.get("locations"):
                loc = data["locations"][-1]
                lat, lon = loc["latitude"], loc["longitude"]
                return lat, lon
        except Exception as e:
            logging.error(f"project44 location fetch failed: {e}")
        return None, None
    # Add more providers here (FourKites, DHL, etc.)
    else:
        logging.warning(f"Provider {provider} not supported.")
        return None, None

def load_inventory(path="data/inventory.json", use_gsheet=False, gsheet_id=None, worksheet_name="Sheet1"):
    if use_gsheet and gsheet_id:
        try:
            import gspread
            from google.oauth2.service_account import Credentials
            # Path to your service account key file
            creds_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "service_account.json")
            scopes = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
            creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
            gc = gspread.authorize(creds)
            sh = gc.open_by_key(gsheet_id)
            worksheet = sh.worksheet(worksheet_name)
            records = worksheet.get_all_records()
            return records
        except Exception as e:
            logging.error(f"Google Sheets load failed: {e}, falling back to local JSON.")
    if not os.path.exists(path):
        logging.warning(f"Inventory file not found: {path}")
        return []
    with open(path) as f:
        return json.load(f)

def load_vendors(path="data/vendors.csv", use_airtable=False, airtable_api_key=None, airtable_base_id=None, airtable_table_name=None):
    if use_airtable and airtable_api_key and airtable_base_id and airtable_table_name:
        try:
            from pyairtable import Table
            table = Table(airtable_api_key, airtable_base_id, airtable_table_name)
            records = table.all()
            # Flatten AirTable records
            return [rec['fields'] for rec in records]
        except Exception as e:
            logging.error(f"AirTable load failed: {e}, falling back to local CSV.")
    if not os.path.exists(path):
        logging.warning(f"Vendors file not found: {path}")
        return []
    return pd.read_csv(path)

def get_api_keys():
    return {
        "NEWSAPI_KEY": os.getenv("NEWSAPI_KEY"),
        "TWITTER_API_KEY": os.getenv("TWITTER_API_KEY"),
        "TWITTER_API_SECRET": os.getenv("TWITTER_API_SECRET"),
        "WEATHERSTACK_KEY": os.getenv("WEATHERSTACK_KEY"),
        "AVIATIONSTACK_KEY": os.getenv("AVIATIONSTACK_KEY"),
        "MYSHIPTRACKING_KEY": os.getenv("MYSHIPTRACKING_KEY"),
        "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    } 