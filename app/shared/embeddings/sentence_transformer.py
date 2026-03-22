from sentence_transformer import SentenceTransformer

def embed_text(text: str)-> list[float]:
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embedding = model.encode(text)
    return embedding.tolist()