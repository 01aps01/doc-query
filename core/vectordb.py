import os
from dotenv import load_dotenv
import pinecone
from pinecone import ServerlessSpec

load_dotenv()

PINECONE_API = os.getenv("PINECONE_API_KEY")
PINECONE_ENV = os.getenv("PINECONE_ENVIRONMENT")  
INDEX_NAME = os.getenv("PINECONE_INDEX", "pdf-index")


def init_pinecone():
    """
    Initialize Pinecone, create index if it doesn't exist,
    and return the Index object.
    """

    pc = pinecone.Pinecone(api_key=PINECONE_API)

    existing_indexes = [idx["name"] for idx in pc.list_indexes()]

    if INDEX_NAME not in existing_indexes:
        pc.create_index(
            name=INDEX_NAME,
            dimension=384,          
            metric="cosine",
            spec=ServerlessSpec(
                cloud="aws",
                region=PINECONE_ENV,
            )
        )

    return pc.Index(INDEX_NAME)


def upsert_vectors(vectors):
    """
    Upsert vectors into Pinecone
    vectors = [(id, embedding, metadata), ...]
    """

    pc = pinecone.Pinecone(api_key=PINECONE_API)
    index = pc.Index(INDEX_NAME)

    index.upsert(
        vectors=[(vid, emb, meta) for vid, emb, meta in vectors]
    )
