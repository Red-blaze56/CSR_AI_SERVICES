from app.modules.generate_campaigns.schema import CampaignGenerationRequest
from app.shared.clients.groq_client import client
from app.modules.generate_campaigns.prompts import generate_campaigns_prompt
from app.shared.utils.json_parser import parse_json
from app.core.config import CONFIG

class CampaignGenerator:
    def __init__(self):
        self.client = client

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
        result = parse_json(raw)
        return result.get("campaigns", [])