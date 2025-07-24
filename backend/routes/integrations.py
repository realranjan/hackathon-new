import os
import requests
from fastapi import APIRouter
from datetime import datetime, timedelta
from supabase import create_client, Client

integrations_router = APIRouter()

@integrations_router.get("/check_integrations")
async def check_integrations():
    status = {}
    # NewsAPI
    news_key = os.getenv("NEWSAPI_KEY")
    if news_key:
        try:
            resp = requests.get("https://newsapi.org/v2/top-headlines", params={"apiKey": news_key, "q": "supply chain", "pageSize": 1})
            status["NewsAPI"] = resp.status_code == 200
        except Exception:
            status["NewsAPI"] = False
    else:
        status["NewsAPI"] = False
    # WeatherStack
    weather_key = os.getenv("WEATHERSTACK_KEY")
    if weather_key:
        try:
            resp = requests.get("http://api.weatherstack.com/current", params={"access_key": weather_key, "query": "Bangalore"})
            status["WeatherStack"] = resp.status_code == 200
        except Exception:
            status["WeatherStack"] = False
    else:
        status["WeatherStack"] = False
    # Twitter
    twitter_key = os.getenv("TWITTER_API_KEY")
    twitter_secret = os.getenv("TWITTER_API_SECRET")
    status["Twitter"] = bool(twitter_key and twitter_secret)
    # AviationStack
    aviation_key = os.getenv("AVIATIONSTACK_KEY")
    if aviation_key:
        try:
            resp = requests.get("http://api.aviationstack.com/v1/flights", params={"access_key": aviation_key, "limit": 1})
            status["AviationStack"] = resp.status_code == 200
        except Exception:
            status["AviationStack"] = False
    else:
        status["AviationStack"] = False
    # MyShipTracking
    ship_key = os.getenv("MYSHIPTRACKING_KEY")
    status["MyShipTracking"] = bool(ship_key)
    # Traccar
    traccar_api = os.getenv("TRACCAR_API", "https://demo.traccar.org/api")
    traccar_user = os.getenv("TRACCAR_USER")
    traccar_pass = os.getenv("TRACCAR_PASS")
    traccar_status = False
    traccar_live = False
    if traccar_api and traccar_user and traccar_pass:
        try:
            resp = requests.get(f"{traccar_api}/devices", auth=(traccar_user, traccar_pass))
            if resp.status_code == 200:
                traccar_status = True
                devices = resp.json()
                now = datetime.utcnow()
                for dev in devices:
                    last_update = dev.get("lastUpdate")
                    if last_update:
                        try:
                            dt = datetime.strptime(last_update[:19], "%Y-%m-%dT%H:%M:%S")
                            if (now - dt) < timedelta(minutes=10):
                                traccar_live = True
                                break
                        except Exception:
                            continue
        except Exception:
            traccar_status = False
    status["Traccar_API"] = traccar_status
    status["Traccar_Live_Device"] = traccar_live
    # Google Sheets
    gsheet_id = os.getenv("GSHEET_ID")
    status["GoogleSheets"] = bool(gsheet_id)
    # Airtable
    airtable_key = os.getenv("AIRTABLE_API_KEY")
    airtable_base = os.getenv("AIRTABLE_BASE_ID")
    airtable_table = os.getenv("AIRTABLE_TABLE_NAME")
    status["Airtable"] = bool(airtable_key and airtable_base and airtable_table)
    # Email/SMTP
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    status["SMTP"] = bool(smtp_server and smtp_user and smtp_pass)
    # Slack
    slack_token = os.getenv("SLACK_TOKEN")
    status["Slack"] = bool(slack_token)
    # Twilio
    twilio_sid = os.getenv("TWILIO_SID")
    twilio_token = os.getenv("TWILIO_TOKEN")
    twilio_from = os.getenv("TWILIO_FROM")
    status["Twilio"] = bool(twilio_sid and twilio_token and twilio_from)
    # LLM
    groq_key = os.getenv("GROQ_API_KEY")
    status["LLM_Groq"] = bool(groq_key)
    # Supabase
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_SERVICE_KEY")
    try:
        supabase = create_client(supabase_url, supabase_key)
        # Try a simple select
        users = supabase.table("user").select("id").limit(1).execute().data
        status["Supabase"] = True if users is not None else False
    except Exception as e:
        status["Supabase"] = False
    return {"integration_status": status} 