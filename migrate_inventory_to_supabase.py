import json
import os
from supabase import create_client
from dotenv import load_dotenv

# Explicitly load .env from backend/
load_dotenv(dotenv_path=os.path.join("backend", ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")

if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
    raise RuntimeError("Supabase credentials not set in environment variables.")

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

with open("data/inventory.json") as f:
    inventory = json.load(f)

success = 0
fail = 0
for item in inventory:
    try:
        # Insert into 'shipment' table
        resp = supabase.table("shipment").insert(item).execute()
        if resp.data:
            print(f"Inserted: {item['product_id']}")
            success += 1
        else:
            print(f"Failed to insert: {item['product_id']} | Error: {resp}")
            fail += 1
    except Exception as e:
        print(f"Exception for {item['product_id']}: {e}")
        fail += 1

print(f"Done. Success: {success}, Fail: {fail}") 