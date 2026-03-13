from google import genai
from app.config.settings import CONFIG

MODEL = CONFIG.GEMINI_MODEL
client = genai.Client(api_key=CONFIG.GEMINI_API_KEY)
async def gemini_generate_response(prompt: str)->str:
    response = await client.aio.models.generate_content(
        model=MODEL,
        contents=prompt
    )
    return response.text
