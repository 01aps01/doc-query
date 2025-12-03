from sentence_transformers import SentenceTransformer

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(EMBED_MODEL)


def embed_texts(texts):
    """
    Takes a list of text strings and returns a list of 384-dim embeddings.
    This uses a local HuggingFace model — no API cost, no rate limits.
    """
    if not texts:
        return []

    embeddings = model.encode(texts, convert_to_numpy=True)

    return embeddings
