import os
import logging
import datetime
from supabase import create_client
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join("backend", ".env"))
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

def log_audit(action, actor, target=None, details=None, log_dir=None):
    entry = {
        "action": action,
        "actor": actor,
        "target": target,
        "details": details,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    try:
        supabase.table("audit_log").insert(entry).execute()
        return True
    except Exception as e:
        logging.error(f"Failed to log audit entry: {e}")
        return False