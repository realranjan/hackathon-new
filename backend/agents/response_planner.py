import os
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from dotenv import load_dotenv
import logging
import functools
import datetime
import json

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

llm_prompt = PromptTemplate(
    input_variables=["risk_report"],
    template="""
You are an expert AI assistant in supply chain risk mitigation. You will evaluate the following list of supply chain risk items. Each item includes:
- product_id: Unique identifier of the product
- risk_score: Integer from 0 to 100 indicating severity
- impact_level: One of ["Low", "Medium", "High"]
- delay_estimate: Estimated delay in days
- cost_impact: Estimated cost impact in USD
- escalation: Boolean or escalation detail
- summary: Short description of the issue

{risk_report}

Your task is to return a JSON array where each object represents a structured action plan per risk item, using the following fields:

- "product_id": Copy directly from input.
- "recommended_actions": A list of **clear, practical mitigation steps**. If rerouting is proposed, specify exact ports, cities, or logistic paths (e.g., "Reroute via Chennai Port instead of Bangalore Port").
- "responsible_party": Assign to the most appropriate actor (e.g., "logistics team", "vendor", "regional supply manager").
- "priority": Determine as "High", "Medium", or "Low" based on both `risk_score` and `impact_level`.
- "escalation": State who or what the issue should be escalated to (e.g., "Escalate to Regional Ops Director"), or use "None" if no escalation is needed.
- "summary": Write a concise 1–2 sentence plan outlining the response strategy.

**Guidelines**:
- Think logically and prioritize realism and feasibility.
- Ensure the recommended actions directly address delay and cost.
- **You must always return at least one action plan per risk item.**
- If you cannot recommend actions, explain why in the summary field.
- Output must be a valid raw JSON array with no markdown, comments, or formatting—**only JSON**.

Return only the JSON array.
"""
)


if not GROQ_API_KEY:
    logging.warning("GROQ_API_KEY not set. LLM-based action planning will use fallback.")

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
def generate_action_plan(risk_report):
    log_agent("generate_action_plan_called", risk_report=risk_report)
    if not risk_report:
        return []
    if not GROQ_API_KEY:
        logging.error("GROQ_API_KEY not set. LLM-based action planning is required.")
        raise RuntimeError("GROQ_API_KEY not set. LLM-based action planning is required.")
    log_agent("llm_input_for_action_plan", risk_report=risk_report)
    try:
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")
        chain = LLMChain(llm=llm, prompt=llm_prompt)
        # Use strict JSON for LLM input
        result = chain.run(risk_report=json.dumps(risk_report))
        log_agent("llm_raw_output_for_action_plan", result=result)
        raw_result = result.strip()
        try:
            plans = json.loads(raw_result)
            if not isinstance(plans, list):
                if isinstance(plans, dict):
                    plans = [plans]
                else:
                    logging.error(f"LLM returned invalid format: {type(plans)}. Output: {raw_result}")
                    raise RuntimeError(f"LLM returned invalid format: {type(plans)}. Output: {raw_result}")
        except Exception as e:
            logging.error(f"LLM did not return valid JSON: {e}. Output: {raw_result}")
            import re
            fixed = re.sub(r',\s*([}}\]])', r'\1', raw_result)
            try:
                plans = json.loads(fixed)
                if not isinstance(plans, list):
                    if isinstance(plans, dict):
                        plans = [plans]
                    else:
                        logging.error(f"LLM returned invalid format after fix: {type(plans)}. Output: {fixed}")
                        raise RuntimeError(f"LLM returned invalid format after fix: {type(plans)}. Output: {fixed}")
            except Exception as e2:
                logging.error(f"LLM JSON fix attempt failed: {e2}. Output: {fixed}")
                raise RuntimeError(f"LLM JSON fix attempt failed: {e2}. Output: {fixed}")
        for i, plan in enumerate(plans):
            if 'risk_score' not in plan and i < len(risk_report):
                plan['risk_score'] = risk_report[i].get('risk_score', 0)
            if 'summary' not in plan and i < len(risk_report):
                plan['summary'] = risk_report[i].get('summary', '')
        log_agent("final_action_plans", plans=plans)
        return plans
    except Exception as e:
        log_agent("llm_action_plan_failed", error=str(e))
        raise RuntimeError(f"LLM action plan failed. Error: {e}")