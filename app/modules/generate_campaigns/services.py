from schema import CampaignGenerationRequest
from shared.clients.groq_client import client
from prompts import generate_campaigns_prompt
from shared.utils import json_parser
from core.config import CONFIG

class CampaignGenerator:
    def __init__(self):
        self.client = client()

    async def groq_generate_response(self, prompt: str) -> str:
        completion = await self.client.chat.completions.create(
            model=CONFIG.GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}]
        )
        return completion.choices[0].message.content

    async def generate_campaigns(self, demands: CampaignGenerationRequest):
        prompt = generate_campaigns_prompt(demands)
        try:
            raw = await self.groq_generate_response(prompt)
        except Exception as e:
            print(f"Error generating campaigns: {e}")
            return []
        result = json_parser(raw)
        return result.get("campaigns", [])


SCHEDULE_VII = """
Schedule VII Categories (Companies Act 2013):
i   - Hunger, poverty, malnutrition, health, sanitation
ii  - Education, vocational skills, livelihood
iii - Gender equality, women empowerment
iv  - Environment, ecology, conservation
v   - National heritage, art, culture
vi  - Armed forces veterans
vii - Rural/Olympic/Paralympic sports
viii- Technology incubators
ix  - Rural development
x   - Slum development
xi  - Disaster management
xii - Other (PM Relief Fund)
"""

def _safe_int(value, default: int) -> int:
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


