import pandas as pd
import json
import os
import logging
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

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
    Use LLM to calculate risk for each shipment/disruption pair. No manual if/else logic.
    For every disruption, match all shipments whose route, current_location, or any leg matches the disruption location.
    """
    if not isinstance(disruptions, list):
        disruptions = [disruptions]
    if not os.path.exists(inventory_path) or not os.path.exists(vendors_path):
        logging.warning(f"Missing inventory or vendors file: {inventory_path}, {vendors_path}")
        return []
    with open(inventory_path) as f:
        inventory = json.load(f)
    vendors = pd.read_csv(vendors_path)
    llm_input = []
    for disruption in disruptions:
        event_loc = disruption.get('location', '').lower()
        for item in inventory:
            # Match if disruption location is in route, current_location, or any leg (fuzzy, case-insensitive)
            match = False
            # Route
            if 'route' in item and isinstance(item['route'], list):
                for loc in item['route']:
                    if event_loc in loc.lower() or loc.lower() in event_loc:
                        match = True
                        break
            # Current location
            if not match and 'current_location' in item and item['current_location']:
                cloc = item['current_location'].lower()
                if event_loc in cloc or cloc in event_loc:
                    match = True
            # Legs
            if not match and 'legs' in item and isinstance(item['legs'], list):
                for leg in item['legs']:
                    for key in ['origin', 'destination', 'current_location']:
                        lloc = leg.get(key)
                        if lloc and (event_loc in lloc.lower() or lloc.lower() in event_loc):
                            match = True
                            break
                    if match:
                        break
            if match:
                vendor_info = {}
                if 'vendor_id' in item:
                    vendor_rows = vendors[vendors['vendor_id'] == item['vendor_id']]
                    if not vendor_rows.empty:
                        vendor_info = vendor_rows.iloc[0].to_dict()
                llm_input.append({
                    "shipment": item,
                    "vendor": vendor_info,
                    "disruption": disruption
                })
    if not llm_input:
        return []
    if GROQ_API_KEY:
        try:
            llm_prompt = PromptTemplate(
                input_variables=["llm_input"],
                template="""
You are a supply chain risk analyst AI. For each shipment/disruption/vendor triple below, assess the risk:
- shipment: dict with product_id, route, current_location, status, etc.
- vendor: dict with vendor_id, status, location, etc.
- disruption: dict with event_type, location, severity, etc.
For each, output a JSON object with:
- product_id
- risk_score (0-100)
- impact_level (Low/Medium/High/Critical)
- delay_estimate (text)
- cost_impact (number)
- escalation (if any)
- summary (1-2 sentences)
Input:
{llm_input}

If the input is empty, output an empty JSON list: []

IMPORTANT: Output ONLY valid JSON, with no explanation, markdown, or code block. Do NOT include any text, comments, or formatting outside the JSON.
"""
            )
            llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
            chain = LLMChain(llm=llm_prompt, prompt=llm_prompt)
            result = chain.run(llm_input=str(llm_input))
            import json as _json
            try:
                risk_reports = _json.loads(result)
            except Exception as e:
                logging.error(f"LLM did not return valid JSON: {e}. Output: {result}")
                risk_reports = []
            return risk_reports
        except Exception as e:
            logging.error(f"LLM risk analysis failed, falling back. Error: {e}")
            return []
    else:
        logging.warning("GROQ_API_KEY not set. LLM-based risk analysis will not run.")
        return [] 