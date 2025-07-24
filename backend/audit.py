import os
import json
import logging
import datetime
from pathlib import Path

def log_audit(action, actor, target=None, details=None, log_dir=None):
    # Use the specified log directory or default to the current directory
    if log_dir is None:
        log_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ensure log directory exists
    os.makedirs(log_dir, exist_ok=True)
    
    AUDIT_LOG_FILE = os.path.join(log_dir, "audit_log.json")
    
    entry = {
        "action": action,
        "actor": actor,
        "target": target,
        "details": details,
        "timestamp": datetime.datetime.utcnow().isoformat()
    }
    
    try:
        # Rotate log if >1MB
        if os.path.exists(AUDIT_LOG_FILE) and os.path.getsize(AUDIT_LOG_FILE) > 1024*1024:
            i = 1
            while os.path.exists(os.path.join(log_dir, f"audit_log_{i}.json")):
                i += 1
            os.rename(AUDIT_LOG_FILE, os.path.join(log_dir, f"audit_log_{i}.json"))
        
        # Load existing log or create new one
        if os.path.exists(AUDIT_LOG_FILE):
            try:
                with open(AUDIT_LOG_FILE, "r") as f:
                    log = json.load(f)
            except json.JSONDecodeError:
                logging.warning(f"Corrupted audit log file: {AUDIT_LOG_FILE}. Creating new log.")
                log = []
        else:
            log = []
        
        # Append new entry and write back
        log.append(entry)
        with open(AUDIT_LOG_FILE, "w") as f:
            json.dump(log, f, indent=2)
            
        return True
    except Exception as e:
        logging.error(f"Failed to log audit entry: {e}")
        return False