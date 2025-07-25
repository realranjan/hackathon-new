import os
import requests
from fastapi import APIRouter
from datetime import datetime, timedelta
from supabase import create_client, Client

integrations_router = APIRouter()

# Removed duplicate /check_integrations endpoint. Use the one in analytics.py 