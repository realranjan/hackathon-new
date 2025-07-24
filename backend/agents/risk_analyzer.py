import pandas as pd
import json
import os
import logging
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import functools
import datetime
from utils.data_loader import load_inventory, load_vendors
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
# Remove legacy comments about inventory.json and vendors.csv
# All data is now loaded from Supabase using load_inventory and load_vendors

def calculate_risk_score(severity, criticality):
    # Simple scoring: High=80, Medium=50, Low=20, scaled by criticality (0-100)
    base = {"High": 80, "Medium": 50, "Low": 20}.get(severity, 30)
    return min(100, int(base + 0.2 * criticality))

def generate_fallback_risk_reports(llm_input):
    """
    Generate risk reports using a rule-based approach when LLM is unavailable.
    This serves as a fallback mechanism when the GROQ API is unavailable or the API key is missing.

    Args:
        llm_input (list): List of input dictionaries, each with 'shipment' and 'disruption' subfields.

    Returns:
        list: List of structured risk report dictionaries.
    """
    
    def calculate_risk_score(severity_level, criticality_score):
        severity_weights = {"Low": 30, "Medium": 60, "High": 90}
        severity_score = severity_weights.get(severity_level, 50)
        return min(100, round(0.6 * severity_score + 0.4 * criticality_score))

    impact_thresholds = [
        (80, "Critical"),
        (60, "High"),
        (40, "Medium"),
        (0,  "Low"),
    ]

    delay_map = {
        "Strike": {"High": "7-10 days", "Medium": "3-5 days", "Low": "1-2 days"},
        "Weather": {"High": "5-7 days", "Medium": "2-4 days", "Low": "1 day"},
        "Port Congestion": {"High": "10-14 days", "Medium": "5-7 days", "Low": "2-3 days"},
        "Political Unrest": {"High": "14+ days", "Medium": "7-10 days", "Low": "3-5 days"}
    }

    risk_reports = []

    for item in llm_input:
        shipment = item.get("shipment", {})
        disruption = item.get("disruption", {})
        
        product_id = shipment.get("product_id", "unknown")
        criticality = shipment.get("criticality_score", 50)
        severity = disruption.get("severity", "Medium")
        event_type = disruption.get("event_type", "Unknown")
        
        risk_score = calculate_risk_score(severity, criticality)
        
        impact_level = next(
            level for threshold, level in impact_thresholds if risk_score >= threshold
        )

        delay_estimate = delay_map.get(event_type, {}).get(severity, "2-5 days")
        cost_impact = int((risk_score / 100) * criticality * 1000)
        
        escalation = (
            "Notify management and activate contingency plan"
            if risk_score >= 70 else "None"
        )

        summary = (
            f"{event_type} event with {severity} severity affecting shipment {product_id}. "
            f"Expected delay of {delay_estimate} with estimated cost impact of ${cost_impact}."
        )
        
        risk_reports.append({
            "product_id": product_id,
            "risk_score": risk_score,
            "impact_level": impact_level,
            "delay_estimate": delay_estimate,
            "cost_impact": cost_impact,
            "escalation": escalation,
            "summary": summary
        })
    
    return risk_reports


def detailed_log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logging.info(f"[ENTER] {func.__name__} args={args} kwargs={kwargs}")
        print(f"[ENTER] {func.__name__} args={args} kwargs={kwargs}")
        try:
            result = func(*args, **kwargs)
            logging.info(f"[EXIT] {func.__name__} returned {result}")
            print(f"[EXIT] {func.__name__} returned {result}")
            return result
        except Exception as e:
            logging.error(f"[ERROR] {func.__name__} exception: {e}", exc_info=True)
            print(f"[ERROR] {func.__name__} exception: {e}")
            raise
    return wrapper

def log_agent(event, **kwargs):
    ts = datetime.datetime.now().isoformat()
    print(f"[AGENT] {ts} | {event} | " + " | ".join(f"{k}={v}" for k, v in kwargs.items()))

@detailed_log
def analyze_risk(disruptions):
    log_agent("analyze_risk_called", disruptions=disruptions)
    if not isinstance(disruptions, list):
        disruptions = [disruptions]

    try:
        inventory = load_inventory()
        vendors = load_vendors()
    except Exception as e:
        logging.error(f"Error loading data from Supabase: {e}")
        return []

    llm_input = []
    for disruption in disruptions:
        event_loc = disruption.get('location', '').lower()
        for item in inventory:
            if _location_matches(event_loc, item):
                vendor_info = _get_vendor_info(item.get('vendor_id'), vendors)
                llm_input.append({
                    "shipment": item,
                    "vendor": vendor_info,
                    "disruption": disruption
                })

    if not llm_input:
        return []

    if not GROQ_API_KEY:
        raise RuntimeError("GROQ_API_KEY not set. LLM-based risk analysis is required.")

    # Log the LLM input
    log_agent("llm_input_for_risk_analysis", llm_input=llm_input)
    print("[DEBUG] LLM INPUT:", json.dumps(llm_input, indent=2))

    try:
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
        chain = LLMChain(llm=llm, prompt=_get_risk_analysis_prompt())
        # Use strict JSON for LLM input
        result = chain.run(llm_input=json.dumps(llm_input))
        log_agent("llm_raw_output_for_risk_analysis", result=result)
        risk_reports = json.loads(result)
        if not isinstance(risk_reports, list):
            raise ValueError("LLM output is not a list")
        for report in risk_reports:
            if not isinstance(report, dict):
                continue
            report['risk_score'] = min(100, max(0, int(report.get('risk_score', 50))))
            if 'summary' not in report:
                report['summary'] = f"Risk analysis for product {report.get('product_id', 'unknown')}"
        log_agent("final_risk_reports", risk_reports=risk_reports)
        return risk_reports
    except Exception as e:
        log_agent("llm_risk_analysis_failed", error=str(e))
        raise RuntimeError(f"LLM risk analysis failed: {e}")

def _location_matches(event_loc, item):
    """Check if disruption location matches any shipment location."""
    # Check route
    if 'route' in item and isinstance(item['route'], list):
        if any(event_loc in loc.lower() or loc.lower() in event_loc for loc in item['route']):
            return True
    
    # Check current location
    if 'current_location' in item and item['current_location']:
        cloc = item['current_location'].lower()
        if event_loc in cloc or cloc in event_loc:
            return True
    
    # Check legs
    if 'legs' in item and isinstance(item['legs'], list):
        for leg in item['legs']:
            for key in ['origin', 'destination', 'current_location']:
                val = leg.get(key)
                if val is not None:
                    lloc = str(val).lower()
                if lloc and (event_loc in lloc or lloc in event_loc):
                    return True
    return False

def _get_vendor_info(vendor_id, vendors):
    """Get vendor information from vendors DataFrame."""
    if vendor_id is None:
        return {}
    vendor_rows = vendors[vendors['vendor_id'] == vendor_id]
    return vendor_rows.iloc[0].to_dict() if not vendor_rows.empty else {}

def _get_risk_analysis_prompt():
    """Return the enhanced prompt template for structured supply chain risk analysis."""
    return PromptTemplate(
        input_variables=["llm_input"],
        template="""
You are an AI supply chain risk analyst. Analyze the following data, which may include information about shipments, disruptions, vendors, or logistics incidents:

Input Data:
{llm_input}

For each item in the input, generate a corresponding JSON object with the following fields:

- \"product_id\": Unique product identifier from the item.
- \"risk_score\": Integer between 0 and 100, based on severity of the disruption and criticality of the shipment.
- \"impact_level\": One of [\"Low\", \"Medium\", \"High\", \"Critical\"], derived from the risk_score using consistent thresholds.
- \"delay_estimate\": Estimated shipping delay in days (integer or range).
- \"cost_impact\": Estimated cost impact in USD.
- \"escalation\": Escalation action required, or \"None\" if not needed. Be specific if escalation is necessary (e.g., \"Notify VP of Global Ops\").
- \"summary\": A concise 1–2 sentence explanation summarizing the risk and suggested action focus.

Instructions:
- Derive values logically from the input context.
- Use consistent logic to map `risk_score` to `impact_level` (e.g., 0–25=Low, 26–50=Medium, 51–75=High, 76–100=Critical).
- Focus on realism and actionable insights.
- **You must always return at least one risk report per input item.**
- If you cannot assess risk, explain why in the summary field.

Output Requirements:
- Output a **JSON array** of the generated objects, one per item.
- Do **not** include any additional explanation, markdown, or code block—only valid raw JSON.
"""
    )
