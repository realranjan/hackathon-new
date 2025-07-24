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
Given this risk report (a list, each item includes shipping_origin, destination, current_location, route, status, disruption, vendor, and escalation if present):
{risk_report}

For each affected shipment, output a JSON object with the specified fields.
If the risk report is empty, output an empty JSON list: []

IMPORTANT: Output ONLY valid JSON, with no explanation, markdown, or code block. Do NOT include any text, comments, or formatting outside the JSON.
"""
)

if not GROQ_API_KEY:
    logging.warning("GROQ_API_KEY not set. LLM-based action planning will use fallback.")

def generate_action_plan(risk_report):
    if not risk_report:
        return []
    # Use LLM if API key is available
    if GROQ_API_KEY:
        try:
            llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
            chain = LLMChain(llm=llm, prompt=llm_prompt)
            result = chain.run(risk_report=str(risk_report))
            import json
            raw_result = result.strip()
            try:
                plans = json.loads(raw_result)
            except Exception as e:
                logging.error(f"LLM did not return valid JSON: {e}. Output: {raw_result}")
                # Try to fix common JSON issues (remove trailing commas)
                import re
                fixed = re.sub(r',\s*([}\]])', r'\1', raw_result)
                try:
                    plans = json.loads(fixed)
                except Exception as e2:
                    logging.error(f"LLM JSON fix attempt failed: {e2}. Output: {fixed}")
                    raise RuntimeError(f"LLM did not return valid JSON. Raw output: {raw_result}")
            # Add risk_score and summary for each plan if not present
            for i, plan in enumerate(plans):
                if 'risk_score' not in plan and i < len(risk_report):
                    plan['risk_score'] = risk_report[i].get('risk_score', 0)
                if 'summary' not in plan and i < len(risk_report):
                    plan['summary'] = risk_report[i].get('summary', '')
            return plans
        except Exception as e:
            logging.error(f"LLM action plan failed. Error: {e}")
            raise RuntimeError(f"LLM action plan failed: {e}")
    else:
        logging.error("GROQ_API_KEY not set. LLM-based action planning will not run.")
        raise RuntimeError("GROQ_API_KEY not set. LLM-based action planning will not run.") 