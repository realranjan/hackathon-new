import datetime
from utils.data_loader import get_api_keys
import httpx
import logging
import tweepy
import time
import random
import os
import json
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join("backend", ".env"))
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

API_KEYS = get_api_keys()
REQUIRED_KEYS = ["NEWSAPI_KEY", "WEATHERSTACK_KEY", "TWITTER_API_KEY", "TWITTER_API_SECRET"]
for k in REQUIRED_KEYS:
    if not API_KEYS.get(k):
        logging.warning(f"Missing API key: {k}. Some features may not work.")

NEWSAPI_URL = "https://newsapi.org/v2/top-headlines"
WEATHERSTACK_URL = "http://api.weatherstack.com/current"
# Twitter API v2 would require OAuth2, here we just show structure

# Helper to parse news articles for disruptions
DISRUPTION_KEYWORDS = [
    "strike", "port closure", "disaster", "protest", "shutdown", "instability", "earthquake", "flood", "hurricane"
]

logging.basicConfig(level=logging.INFO)

async def fetch_news_events(location="India"):
    api_key = API_KEYS.get("NEWSAPI_KEY")
    if not api_key:
        logging.warning("Missing NEWSAPI_KEY.")
        return []
    params = {
        "apiKey": api_key,
        "q": " OR ".join(DISRUPTION_KEYWORDS),
        "language": "en",
        "pageSize": 5,
        "country": "in"
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(NEWSAPI_URL, params=params, timeout=10)
            if resp.status_code == 200:
                articles = resp.json().get("articles", [])
                events = []
                for art in articles:
                    for kw in DISRUPTION_KEYWORDS:
                        if kw in art["title"].lower() or kw in art.get("description", "").lower():
                            events.append({
                                "location": location,
                                "event_type": kw.title(),
                                "severity": "High",
                                "timestamp": art["publishedAt"],
                                "source": art["url"],
                                "data_source": "real"
                            })
                            break
                logging.info(f"NewsAPI events found: {len(events)}")
                return events
            else:
                logging.warning(f"NewsAPI error: {resp.status_code} {resp.text}")
    except Exception as e:
        logging.error(f"NewsAPI fetch failed: {e}")
    return []

async def fetch_weather_events(location="Bangalore"):
    api_key = API_KEYS.get("WEATHERSTACK_KEY")
    if not api_key:
        logging.warning("Missing WEATHERSTACK_KEY.")
        return []
    params = {
        "access_key": api_key,
        "query": location
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(WEATHERSTACK_URL, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                weather_desc = data.get("current", {}).get("weather_descriptions", [""])[0].lower()
                for kw in ["storm", "flood", "hurricane", "cyclone", "disaster"]:
                    if kw in weather_desc:
                        event = {
                            "location": location,
                            "event_type": kw.title(),
                            "severity": "High",
                            "timestamp": datetime.datetime.utcnow().isoformat(),
                            "source": "WeatherStack",
                            "data_source": "real"
                        }
                        logging.info(f"WeatherStack event found: {event}")
                        return [event]
            else:
                logging.warning(f"WeatherStack error: {resp.status_code} {resp.text}")
    except Exception as e:
        logging.error(f"WeatherStack fetch failed: {e}")
    return []

def fetch_twitter_events(query="port OR strike OR closure OR disaster", location="India", count=5):
    api_key = API_KEYS.get("TWITTER_API_KEY")
    api_secret = API_KEYS.get("TWITTER_API_SECRET")
    if not api_key or not api_secret:
        logging.warning("Missing TWITTER_API_KEY or TWITTER_API_SECRET.")
        return []
    try:
        auth = tweepy.AppAuthHandler(api_key, api_secret)
        api = tweepy.API(auth)
        tweets = api.search_tweets(q=query, lang="en", count=count, tweet_mode="extended")
        events = []
        for tweet in tweets:
            text = tweet.full_text.lower()
            for kw in DISRUPTION_KEYWORDS:
                if kw in text:
                    events.append({
                        "location": location,
                        "event_type": kw.title(),
                        "severity": "Medium",
                        "timestamp": str(tweet.created_at),
                        "source": f"https://twitter.com/user/status/{tweet.id}",
                        "data_source": "real"
                    })
                    break
        return events
    except Exception as e:
        logging.error(f"Twitter fetch failed: {e}")
        return []

# Add imports for new APIs
# Add new API URLs
AVIATIONSTACK_URL = "http://api.aviationstack.com/v1/flights"
MYSHIPTRACKING_URL = "https://api.myshiptracking.com/v1/ships"

# Add explicit air, sea, and road event fetchers
async def fetch_air_events(location="India"):
    api_key = API_KEYS.get("AVIATIONSTACK_KEY")
    if not api_key:
        logging.warning("Missing AVIATIONSTACK_KEY.")
        return []
    params = {
        "access_key": api_key,
        "arr_icao": "VIDP",  # Example: Delhi airport ICAO
        "limit": 5
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(AVIATIONSTACK_URL, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                events = []
                for flight in data.get("data", []):
                    if flight.get("flight_status") in ["cancelled", "diverted", "incident"]:
                        event = {
                            "location": flight.get("arrival", {}).get("airport", location),
                            "event_type": flight["flight_status"].title(),
                            "severity": "High",
                            "timestamp": flight.get("arrival", {}).get("estimated", time.strftime("%Y-%m-%dT%H:%M:%SZ")),
                            "source": "AviationStack",
                            "mode": "air",
                            "data_source": "real"
                        }
                        # Add flight_number if available
                        if flight.get("flight", {}).get("iata"):
                            event["flight_number"] = flight["flight"]["iata"]
                        events.append(event)
                logging.info(f"AviationStack air events found: {len(events)}")
                return events
            else:
                logging.warning(f"AviationStack error: {resp.status_code} {resp.text}")
    except Exception as e:
        logging.error(f"AviationStack fetch failed: {e}")
    return []

async def fetch_sea_events(location="China"):
    api_key = API_KEYS.get("MYSHIPTRACKING_KEY")
    if not api_key:
        logging.warning("Missing MYSHIPTRACKING_KEY.")
        return []
    params = {
        "key": api_key,
        "country": "CN",
        "limit": 5
    }
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(MYSHIPTRACKING_URL, params=params, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                events = []
                for ship in data.get("data", []):
                    if ship.get("status") in ["stopped", "distress", "incident"]:
                        event = {
                            "location": ship.get("last_port", location),
                            "event_type": ship["status"].title(),
                            "severity": "High",
                            "timestamp": ship.get("last_update", time.strftime("%Y-%m-%dT%H:%M:%SZ")),
                            "source": "MyShipTracking",
                            "mode": "sea",
                            "data_source": "real"
                        }
                        # Add ship_name and container_id if available
                        if ship.get("ship_name"):
                            event["ship_name"] = ship["ship_name"]
                        if ship.get("container_id"):
                            event["container_id"] = ship["container_id"]
                        events.append(event)
                logging.info(f"MyShipTracking sea events found: {len(events)}")
                return events
            else:
                logging.warning(f"MyShipTracking error: {resp.status_code} {resp.text}")
    except Exception as e:
        logging.error(f"MyShipTracking fetch failed: {e}")
    return []

async def fetch_road_events(location="India"):
    # Use NewsAPI and Twitter for road/land disruptions
    news_events = await fetch_news_events(location)
    twitter_events = fetch_twitter_events(location=location)
    # Tag as road
    for e in news_events:
        e["mode"] = "road"
    for e in twitter_events:
        e["mode"] = "road"
    return news_events + twitter_events

# Update fetch_or_simulate_events to use new agents

async def fetch_or_simulate_events():
    events = []
    try:
        air_events = await fetch_air_events()
        if air_events:
            events.extend(air_events)
    except Exception as e:
        logging.error(f"Air fetch failed: {e}")
    try:
        sea_events = await fetch_sea_events()
        if sea_events:
            events.extend(sea_events)
    except Exception as e:
        logging.error(f"Sea fetch failed: {e}")
    try:
        road_events = await fetch_road_events()
        if road_events:
            events.extend(road_events)
    except Exception as e:
        logging.error(f"Road fetch failed: {e}")
    if not events:
        logging.info("No real events found, using simulation.")
        # --- Dynamic simulation logic ---
        try:
            # Load inventory from Supabase to get possible locations
            shipments = supabase.table("shipment").select("*").execute().data
            locations = set()
            for item in shipments:
                if 'route' in item and item['route']:
                    locations.update(item['route'])
                if 'shipping_origin' in item and item['shipping_origin']:
                    locations.add(item['shipping_origin'])
                if 'destination' in item and item['destination']:
                    locations.add(item['destination'])
                if 'legs' in item and item['legs']:
                    for leg in item['legs']:
                        for key in ['origin', 'destination', 'current_location']:
                            val = leg.get(key)
                            if val:
                                locations.add(val)
            locations = list(locations)
        except Exception as e:
            logging.error(f"Failed to load inventory for simulation: {e}")
            locations = ["Bangalore", "Chennai", "Mumbai", "Delhi", "Pune", "Hyderabad", "Kolkata"]
        # Define possible event types
        event_types = ["Strike", "Flood", "Protest", "Port Congestion", "Political Unrest", "Weather"]
        # Randomly select location and event type
        import random
        sim_location = random.choice(locations) if locations else "Bangalore"
        sim_event_type = random.choice(event_types)
        event_payload = {
            "location": sim_location,
            "event_type": sim_event_type,
            "severity": random.choice(["High", "Medium", "Low"]),
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "source": "Simulated",
            "mode": "road",
            "data_source": "simulated"
        }
        return [event_payload]
    return events

def fetch_or_simulate_events_sync():
    import asyncio
    return asyncio.run(fetch_or_simulate_events()) 