import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import logging

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm_prompt = PromptTemplate(
    input_variables=["risk_report"],
    template="""
Given this risk report (each item includes shipping_origin, destination, current_location, route, and escalation if present):
{risk_report}
For each affected shipment:
- If escalation is present, explain why (e.g., vendor failure, no alternate route).
- Otherwise, suggest alternate shipping routes from current_location to destination (if possible), considering the route and any disruptions.
- Suggest alternate vendors (if available).
- Recommend mitigation steps.
- Generate a notification message for the operations team.
Output as a JSON object with keys: new_route, alt_vendor, mitigation_steps, notification_text, escalation (if any).
"""
)

if not GROQ_API_KEY:
    logging.warning("GROQ_API_KEY not set. LLM-based action planning will use fallback.")

def generate_action_plan(risk_report):
    # Use LLM if API key is available
    if GROQ_API_KEY:
        try:
            llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="mixtral-8x7b-32768")
            chain = LLMChain(llm=llm, prompt=llm_prompt)
            result = chain.run(risk_report=str(risk_report))
            import json
            try:
                plan = json.loads(result)
            except Exception as e:
                logging.error(f"LLM did not return valid JSON: {e}. Output: {result}")
                plan = {}
            # Add risk_score and summary
            if risk_report:
                max_score = max(r['risk_score'] for r in risk_report)
                summary = f"Highest risk score: {max_score}"
            else:
                max_score = 0
                summary = "No risk detected."
            plan["risk_score"] = max_score
            plan["summary"] = summary
            return plan
        except Exception as e:
            logging.error(f"LLM action plan failed, falling back. Error: {e}")
    # Fallback: rule-based
    if risk_report:
        max_score = max(r['risk_score'] for r in risk_report)
        summary = f"Highest risk score: {max_score}"
    else:
        max_score = 0
        summary = "No risk detected."
    return {
        "new_route": None,
        "alt_vendor": None,
        "mitigation_steps": ["Monitor situation", "Contact vendor"],
        "notification_text": summary,
        "risk_score": max_score,
        "summary": summary
    } 