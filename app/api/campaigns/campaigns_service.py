from app.ai.groq_client import groq_generate_response
from app.prompts.csr_prompts import generate_campaigns_prompt
from app.utils.json_parser import parse_json

async def generate_campaigns(preferences: dict) -> list:
    prompt = generate_campaigns_prompt(preferences)
    raw = await groq_generate_response(prompt)
    result = parse_json(raw)
    return result.get("campaigns", [])