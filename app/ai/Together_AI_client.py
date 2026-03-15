from together import AsyncTogether
from app.config.settings import CONFIG

client = AsyncTogether(api_key=CONFIG.TOGETHER_API_KEY)
MODEL = CONFIG.TOGETHER_MODEL

async def together_ai_generate_response(prompt: str) -> str:
    completion = await client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content



