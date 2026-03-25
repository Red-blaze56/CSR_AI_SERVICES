from groq import AsyncGroq
from app.core.config import CONFIG

client = AsyncGroq(api_key=CONFIG.GROQ_API_KEY) 
