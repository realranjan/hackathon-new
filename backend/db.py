import os
from dotenv import load_dotenv
from supabase import create_client, Client
from passlib.context import CryptContext

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
JWT_SECRET = os.getenv("JWT_SECRET", "SECRET")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Example CRUD helpers

def get_all_users():
    return supabase.table("user").select("*").execute().data

def get_user_by_email(email):
    return supabase.table("user").select("*").eq("email", email).single().execute().data

def create_user(user_dict):
    return supabase.table("user").insert(user_dict).execute().data

def get_all_shipments():
    return supabase.table("shipment").select("*").execute().data

def create_shipment(shipment_dict):
    return supabase.table("shipment").insert(shipment_dict).execute().data

def get_all_vendors():
    return supabase.table("vendor").select("*").execute().data

def create_vendor(vendor_dict):
    return supabase.table("vendor").insert(vendor_dict).execute().data