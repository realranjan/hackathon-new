import os
import json

def log_audit(action, actor, target=None, details=None):
    AUDIT_LOG_FILE = "audit_log.json"
    entry = {
        "action": action,
        "actor": actor,
        "target": target,
        "details": details,
        "timestamp": __import__('datetime').datetime.utcnow().isoformat()
    }
    # Rotate log if >1MB
    if os.path.exists(AUDIT_LOG_FILE) and os.path.getsize(AUDIT_LOG_FILE) > 1024*1024:
        i = 1
        while os.path.exists(f"audit_log_{i}.json"):
            i += 1
        os.rename(AUDIT_LOG_FILE, f"audit_log_{i}.json")
    if os.path.exists(AUDIT_LOG_FILE):
        with open(AUDIT_LOG_FILE, "r") as f:
            log = json.load(f)
    else:
        log = []
    log.append(entry)
    with open(AUDIT_LOG_FILE, "w") as f:
        json.dump(log, f, indent=2) 