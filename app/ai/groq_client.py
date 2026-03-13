# app/ai/groq_client.py

from groq import AsyncGroq
from app.config.settings import CONFIG

client = AsyncGroq(api_key=CONFIG.GROQ_API_KEY)
MODEL = CONFIG.GROQ_MODEL

async def groq_generate_response(prompt: str) -> str:
    completion = await client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content