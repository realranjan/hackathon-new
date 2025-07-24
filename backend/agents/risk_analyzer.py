import pandas as pd
import json
import os
import logging

# To use Google Sheets for inventory or Airtable for vendors, import and use the load_inventory/load_vendors functions from utils.data_loader.py
# Example (uncomment and configure as needed):
# from utils.data_loader import load_inventory, load_vendors
# import os
# inventory = load_inventory(
#     use_gsheet=True,
#     gsheet_id=os.getenv("GSHEET_ID"),
#     worksheet_name=os.getenv("GSHEET_WORKSHEET", "Sheet1")
# )
# vendors = load_vendors(
#     use_airtable=True,
#     airtable_api_key=os.getenv("AIRTABLE_API_KEY"),
#     airtable_base_id=os.getenv("AIRTABLE_BASE_ID"),
#     airtable_table_name=os.getenv("AIRTABLE_TABLE_NAME")
# )
# By default, the code below uses local files (data/inventory.json, data/vendors.csv)

def calculate_risk_score(severity, criticality):
    # Simple scoring: High=80, Medium=50, Low=20, scaled by criticality (0-100)
    base = {"High": 80, "Medium": 50, "Low": 20}.get(severity, 30)
    return min(100, int(base + 0.2 * criticality))

def analyze_risk(disruptions, inventory_path="data/inventory.json", vendors_path="data/vendors.csv"):
    """
    disruptions: list of event_payload dicts (can also accept a single dict for backward compatibility)
    Returns a list of risk reports, one per affected shipment/disruption pair, with deduplication, escalation, predictive ETA, and cost impact logic.
    """
    if not isinstance(disruptions, list):
        disruptions = [disruptions]
    if not os.path.exists(inventory_path) or not os.path.exists(vendors_path):
        logging.warning(f"Missing inventory or vendors file: {inventory_path}, {vendors_path}")
        return []
    with open(inventory_path) as f:
        inventory = json.load(f)
    vendors = pd.read_csv(vendors_path)
    risk_reports = []
    seen = set()  # For deduplication
    for item in inventory:
        if 'vendor_id' not in item:
            continue
        vendor_rows = vendors[vendors['vendor_id'] == item['vendor_id']]
        if vendor_rows.empty:
            continue
        vendor_info = vendor_rows.iloc[0]
        # Edge case: vendor failure
        if vendor_info.get('status', '').lower() in ['bankrupt', 'failed', 'inactive']:
            risk_report = {
                "product_id": item['product_id'],
                "vendor": vendor_info['vendor_id'],
                "delay_estimate": "Unknown",
                "impact_level": "Critical",
                "risk_score": 100,
                "escalation": "Vendor failure - escalate to human ops",
                "cost_impact": 10000  # Example: high cost for vendor failure
            }
            risk_reports.append(risk_report)
            continue
        for disruption in disruptions:
            # Deduplicate by event_type, location, and product_id
            dedup_key = (disruption.get('event_type'), disruption.get('location'), item['product_id'])
            if dedup_key in seen:
                continue
            seen.add(dedup_key)
            matched = False
            # Match by container_id, ship_name, or flight_number if present in both event and item
            for key in ["container_id", "ship_name", "flight_number"]:
                if key in disruption and key in item and disruption.get(key) and item.get(key):
                    if disruption[key] == item[key]:
                        matched = True
                        break
            # If not matched by ID, check current_location and route waypoints
            if not matched:
                event_loc = disruption.get('location', '')
                if 'current_location' in item and item['current_location'] and event_loc in item['current_location']:
                    matched = True
                elif 'route' in item and isinstance(item['route'], list) and any(event_loc in wp for wp in item['route']):
                    matched = True
                elif vendor_info['location'] in event_loc:
                    matched = True
            if matched:
                score = calculate_risk_score(disruption['severity'], item['criticality_score'])
                # --- Predictive ETA and Delay Propagation ---
                delay_days = 0
                cost_impact = 0
                if disruption['severity'] == 'High':
                    delay_days = 3
                    cost_impact = 2000
                elif disruption['severity'] == 'Medium':
                    delay_days = 1
                    cost_impact = 500
                # Update ETA for affected leg and propagate
                legs = item.get('legs', [])
                affected_leg = None
                for leg in legs:
                    if event_loc in [leg.get('origin'), leg.get('destination'), leg.get('current_location')]:
                        affected_leg = leg
                        break
                if affected_leg and delay_days > 0:
                    # Update ETA for affected leg
                    try:
                        from datetime import datetime, timedelta
                        eta_dt = datetime.strptime(affected_leg['eta'], "%Y-%m-%d")
                        new_eta = eta_dt + timedelta(days=delay_days)
                        affected_leg['eta'] = new_eta.strftime("%Y-%m-%d")
                        affected_leg['status'] = 'delayed'
                        # Propagate delay to downstream legs
                        propagate = False
                        for leg in legs:
                            if propagate:
                                eta_dt = datetime.strptime(leg['eta'], "%Y-%m-%d")
                                leg['eta'] = (eta_dt + timedelta(days=delay_days)).strftime("%Y-%m-%d")
                            if leg is affected_leg:
                                propagate = True
                    except Exception as e:
                        logging.warning(f"Failed to update ETA for {item['product_id']}: {e}")
                risk_report = {
                    "product_id": item['product_id'],
                    "vendor": vendor_info['vendor_id'],
                    "delay_estimate": f"{delay_days} days" if delay_days else "2-5 days",
                    "impact_level": disruption['severity'],
                    "risk_score": score,
                    "cost_impact": cost_impact
                }
                # Include all relevant info
                for key in ["container_id", "ship_name", "flight_number", "current_location", "route", "shipping_origin", "destination", "status", "legs"]:
                    if key in item:
                        risk_report[key] = item[key]
                # Escalate if no alternate route is possible (demo: if route has only 1 leg left and disruption is at destination)
                if 'route' in item and isinstance(item['route'], list) and len(item['route']) <= 2 and disruption.get('location') == item.get('destination'):
                    risk_report['escalation'] = "No alternate route available - escalate to human ops"
                risk_reports.append(risk_report)
    return risk_reports 