from sentence_transformers import SentenceTransformer
import asyncio

model = SentenceTransformer('all-MiniLM-L6-v2')
def _embed(text: str):
    return model.encode(text, normalize_embeddings=True).tolist()
async def embed_text(text: str) -> list[float]:
    return await asyncio.to_thread(_embed, text)