from app.ai.gemini_client import gemini_generate_response
from app.prompts.csr_prompts import extract_prompt
from app.utils.json_parser import parse_json

async def extract_preferences(message: str, current_step: str) -> dict:
    prompt = extract_prompt(current_step, message)
    raw = await gemini_generate_response(prompt)
    return parse_json(raw)