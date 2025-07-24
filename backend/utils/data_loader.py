import json
import os
from dotenv import load_dotenv
import logging
import requests
from supabase import create_client, Client

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
def update_shipment_location_by_gps(product_id, lat, lon, use_supabase=True):
    """Update a shipment's current_location in Supabase based on GPS coordinates (reverse geocode to city/port)."""
    try:
        # Use OpenStreetMap Nominatim for reverse geocoding
        import requests
        resp = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}")
        city = None
        if resp.status_code == 200:
            data = resp.json()
            city = data.get("address", {}).get("city") or data.get("address", {}).get("town") or data.get("address", {}).get("village") or data.get("display_name")
        if not city:
            city = f"({lat:.2f},{lon:.2f})"
        from supabase import create_client
        import os
        from dotenv import load_dotenv
        load_dotenv(dotenv_path=os.path.join("backend", ".env"))
        SUPABASE_URL = os.getenv("SUPABASE_URL")
        SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
        supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
        resp = supabase.table("shipment").update({"current_location": city}).eq("product_id", product_id).execute()
        if not resp.data:
            import logging
            logging.error(f"Failed to update shipment location in Supabase for {product_id}")
            return None
        return city
    except Exception as e:
        import logging
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

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def load_inventory():
    return supabase.table("shipment").select("*").execute().data

def load_vendors():
    import pandas as pd
    data = supabase.table("vendor").select("*").execute().data
    return pd.DataFrame(data)

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