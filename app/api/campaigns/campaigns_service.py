from app.ai.Together_AI_client import together_ai_generate_response
from app.ai.groq_client import groq_generate_response
from app.prompts.csr_prompts import generate_campaigns_prompt
from app.utils.json_parser import parse_json

async def generate_campaigns(preferences: dict) -> list:
    prompt = generate_campaigns_prompt(preferences)
    try:
        raw = await groq_generate_response(prompt)
    except Exception:
        try:
            raw = await groq_generate_response(prompt)
        except:
            raw = await together_ai_generate_response(prompt)
    result = parse_json(raw)
    return result.get("campaigns", [])